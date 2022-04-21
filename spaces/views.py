import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Count
from django.http      import JsonResponse, HttpResponse
from django.conf      import settings
from django.db        import transaction

from storage              import FileUploader, s3_client
from utilities.decorators import check_token
from spaces.models        import Review, Space, Category, Image
from users.models         import Booking, Host, User

class SpaceView(View):
    def get(self, request):
        offset            = int(request.GET.get('offset', 0))
        limit             = int(request.GET.get('limit', 9))
        order             = request.GET.get('order', None)
        filter_dictionary = request.GET.items()

        FILTER_SET = {
            "capacity": "max_capacity__exact",
            "date"    : "booking__start_time__date",
            "category": "category__title"
        }

        STANDARD = {
            "desc_price": "-price",
            "asc_price" : "price",
        }

        spaces = Space.objects.select_related('category').prefetch_related('images')\
                .annotate(best = Count('wishlists__space'))\
                .filter(**self.create_filters(FILTER_SET, filter_dictionary)).order_by(STANDARD.get(order, '-best'))[offset:offset+limit]

        result = [{
            'id'          : space.id,
            'title'       : space.title,
            'sub_title'   : space.sub_title,
            'room_name'   : space.room_name,
            'price'       : space.price,
            'detail'      : space.detail,
            'max_capacity': space.max_capacity,
            'address'     : space.address,
            'image'       : [image.url for image in space.images.all()],
            'category'    : {
                'category_id'   : space.category.id,
                'category_title': space.category.title
            }
        } for space in spaces]

        return JsonResponse({'result':result}, status=200)
    
    @check_token
    def post(self, request):
        try:
            user = request.user

            if not user.check_host():
                return JsonResponse({'message' : 'HOST_EXIST_ERROR'}, status = 401)
            
            files = request.FILES.getlist('filename', [])

            if not files:
                return JsonResponse({'message' : 'FILE_UPLOAD_ERROR'}, status = 400)

            image_urls = [FileUploader(s3_client, settings.BUCKET_NAME).upload(file, 'gocloud/') for file in files]

            with transaction.atomic():
                space = Space.objects.create(
                    host         = Host.objects.get(user = user),
                    title        = request.POST['title'],
                    sub_title    = request.POST['sub_title'],
                    detail       = request.POST['detail'],
                    max_capacity = request.POST['max_capacity'],
                    address      = request.POST['address'],
                    price        = request.POST['price'],
                    category     = Category.objects.get(title = request.POST['category_title'])
                )
            
                images = [Image(space_id=space.id, url=image_url) for image_url in image_urls]
                Image.objects.bulk_create(images)

            return HttpResponse(status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    def create_filters(self, FILTER_SET, filter_dictionary):
        query = {FILTER_SET[key] : value for key, value in filter_dictionary if FILTER_SET.get(key)}
        return query

class ReviewView(View):
    @check_token
    def post(self, request):
        data      = request.POST
        file      = request.FILES.get('image')

        if file == None:
            return JsonResponse({'mesasage':'FILE_UPLOAD_ERROR'}, status=400)

        image_file = FileUploader(s3_client, settings.BUCKET_NAME).upload(file, 'gocloud/')

        Review.objects.create(
            user   = request.user,
            space  = Space.objects.get(id = data['space_id']),
            content   = data['content'],
            image_url = image_file
        )
        return JsonResponse({'message':'SUCCESS'}, status=200)
            
    def get(self, request):
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 6))
        reviews = Review.objects.all()[offset:offset+limit]
        
        result = [{
            'id':review.id,
            'content': review.content,
            'image'  : review.image_url,
            'space'  : {
                'space_id'  : review.space.id,
                'space_name': review.space.title,
                'price'     : float(review.space.price)}
        } for review in reviews]
        
        return JsonResponse({'result':result}, status=200)

class SpaceDetailView(View):
    def get(self, request, space_id):
        try:
            space = Space.objects.select_related('category').prefetch_related('images').get(id=space_id)

            result = {
                'id'          : space.id,
                'title'       : space.title,
                'sub_title'   : space.sub_title,
                'room_name'   : space.room_name,
                'detail'      : space.detail,
                'max_capacity': space.max_capacity,
                'address'     : space.address,
                'price'       : float(space.price),
                'image'       : [images.url for images in space.images.all()],
                'category'    : space.category.title
            }
        except Space.DoesNotExist:
            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=400)
        return JsonResponse({'result':result}, status=200)

class BookingView(View):
    @check_token
    def post(self, request, space_id):
        try:
            data  = json.loads(request.body)
            user  = request.user
            space = Space.objects.get(id=space_id)

            start_time  = data['start_time']
            finish_time = data['finish_time']
            
            if Booking.objects.filter(user_id = user.id, space_id = space.id, start_time=start_time, finish_time=finish_time).exists():
                return JsonResponse({'message':'ALREADY_EXIST'}, status=400)

            Booking.objects.create(
                user        = user,
                space       = space,
                start_time  = start_time,
                finish_time = finish_time
            )

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Space.DoesNotExist:
            return JsonResponse({'message':'SPACE_DOES_NOT_EXIST'}, status=400)

        return JsonResponse({'message':'SUCCESS'}, status=201)

class BookingListView(View):
    @check_token
    def get(self, request):
        user = request.user
        bookings = Booking.objects.select_related('space').filter(user_id = user.id)

        result = [{
            'id'         : booking.id,
            'space'      : booking.space.title,
            'space_name' : booking.space.room_name,
            'start_time' : booking.start_time,
            'finish_time': booking.finish_time,
            'price'      : booking.space.price,
            'space_id'   : booking.space.id
        } for booking in bookings]
        
        return JsonResponse({'result':result}, status=200)