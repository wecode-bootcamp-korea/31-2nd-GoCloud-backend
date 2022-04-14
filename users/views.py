import jwt, datetime, requests, json

from django.shortcuts import redirect
from django.views import View
from django.http  import JsonResponse, HttpResponse
from django.conf  import settings

from users.models         import User, Host, WishList
from spaces.models        import *
from utilities.decorators import check_token

class KakaoAPI:
    def request_access_token(self, auth_code):
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type'  : 'authorization_code',
            'client_id'   : settings.APP_KEY,
            'code'        : auth_code
        }
        token  = requests.post(kakao_token_api, data=data, timeout=2)
        return token.json()['access_token']

    def request_user_info(self, access_token):
        return requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization" : f'Bearer {access_token}'}).json()

class KakaoSigninView(View):
    def get(self, request): 
        try:
            auth_code    = request.GET.get('code')

            kakao_client = KakaoAPI()

            access_token = kakao_client.request_access_token(auth_code)
            user_info    = kakao_client.request_user_info(access_token)

            kakao_id       = user_info['id']
            kakao_email    = user_info['kakao_account']['email']
            kakao_nickname = user_info['properties']['nickname']

            user  = self.get_or_create(kakao_id, kakao_email, kakao_nickname)
            token = self.generate_jwt(user.id)
            
            return JsonResponse({'token':token}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get_or_create(self, kakao_id, kakao_email, kakao_nickname):
        if not User.objects.filter(kakao_id=kakao_id).exists():
            user = User.objects.create(
                kakao_id = kakao_id,
                nickname = kakao_nickname,
                email    = kakao_email
            )
            
        user = User.objects.get(kakao_id=kakao_id)
        return user

    def generate_jwt(self, user_id):
        return jwt.encode({
            'sub':user_id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, settings.SECRET_KEY, settings.ALGORITHM)

class HostConvertView(View):
    @check_token
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        if Host.objects.filter(user=user).exists():
            return JsonResponse({'message': 'ALREADY_EXISTS'})

        Host.objects.create(
            user = user,
            phone_number = data['phone_number']
        )
        return HttpResponse(status = 201)

class WishListView(View):
    @check_token
    def get(self, request):
        wishlist = WishList.objects.filter(user = request.user)

        wishlist =  [{
            'id' : wish_space.id,
            'space' : {
                'id'          : wish_space.space.id,
                'title'       : wish_space.space.title,
                'sub_title'   : wish_space.space.sub_title,
                'room_name'   : wish_space.space.room_name,
                'detail'      : wish_space.space.detail,
                'max_capacity': wish_space.space.max_capacity,
                'address'     : wish_space.space.address,
                'price'       : wish_space.space.price,
                'category'    : wish_space.space.category.id,
            }
        } for wish_space in wishlist]

        return JsonResponse({'wish_list' : wishlist}, status=200)
        
class PostWishView(View):
    @check_token
    def post(self, request, space_id):
        try:
            space      = Space.objects.get(id = space_id)
            wish_space = WishList.objects.filter(user = request.user, space = space)

            if not wish_space.exists():
                WishList.objects.create(user = request.user, space = space)
                return HttpResponse(status = 201)
            
            wish_space.delete()
            return HttpResponse(status = 204)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)