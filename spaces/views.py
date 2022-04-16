from asyncore import file_dispatcher
import uuid

from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction
from django.db.models import Count
from django.conf      import settings

from storage              import S3Client
from spaces.models        import Space, Review
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
        file      = request.FILES.get('image', None)
        s3_client = S3Client(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

        try:
            with transaction.atomic():
                key = 'review/' + str(uuid.uuid4()) + file.name
                Review.objects.create(
                    user_id   = request.user,
                    space_id  = data['space_id'],
                    content   = data['content'],
                    image_url = settings.STATIC_URL + key
                )
                s3_client.upload(file, key, settings.AWS_STORAGE_BUCKET_NAME)

                return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)