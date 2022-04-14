from django.views     import View
from django.http      import JsonResponse
from django.db.models import Count
from django.conf      import settings

from spaces.models        import Space
from utilities.storages   import s3_client, FileUploader
from .models              import *
from utilities.decorators import check_token

class SpaceListView(View):
    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 20))
        order  = request.GET.get('order', None)
        filter_dictionary = request.GET.items()

        FILTER_SET = {
            "capacity": "max_capacity__exact",
            "date"    : "booking__start_time__date",
            "search"  : "category__id"
        }

        STANDARD = {
            "desc_price": "-price",
            "asc_price" : "price",
        }

        spaces = Space.objects.select_related('category').prefetch_related('images')\
                .annotate(best = Count('wishlists__space'))\
                .filter(**self.create_filters(FILTER_SET, filter_dictionary)).order_by(STANDARD.get(order, '-best'))[offset:offset+limit]

        result = [{
            'title'       : space.title,
            'sub_title'   : space.sub_title,
            'room_name'   : space.room_name,
            'price'       : space.price,
            'detail'      : space.detail,
            'max_capacity': space.max_capacity,
            'address'     : space.address,
            'image'       : [image.url for image in space.images.all()],
            'category'    : space.category.id
        } for space in spaces]

        return JsonResponse({'result':result}, status=200)

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
            user_id   = request.user,
            space_id  = data['space_id'],
            content   = data['content'],
            image_url = image_file
        )
        return JsonResponse({'message':'SUCCESS'}, status=200)
            
    def get(self, request):
        reviews = Review.objects.all()
        
        result = [{
            'id':review.id,
            'content':review.content,
            'image':review.image_url,
            'space':{
                'space_id':review.space.id,
                'space_name':review.space.title,
                'price':float(review.space.price)}
        } for review in reviews]

        return JsonResponse({'result':result}, status=200)