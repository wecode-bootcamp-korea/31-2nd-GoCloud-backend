import jwt, datetime, requests

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from users.models  import User

class KaKaoSigninView(View):
    def get(self, request):
        auth_code    = request.GET.get('code')
        access_token = self.request_access_token(auth_code)
        
        user_info = self.request_user_info(access_token)

        kakao_id       = user_info['id']
        kakao_email    = user_info['kakao_account']['email']
        kakao_nickname = user_info['properties']['nickname']

        user  = self.get_or_create(kakao_id, kakao_email, kakao_nickname)
        token = self.generate_jwt(user.id)

        return JsonResponse({'token':token}, status=200)

    def get_or_create(self, kakao_id, kakao_email, kakao_nickname):
        if not User.objects.filter(kakao_id=kakao_id).exists():
            user = User.objects.create(
                kakao_id = kakao_id,
                nickname = kakao_nickname,
                email    = kakao_email
            )
            
        user      = User.objects.get(kakao_id=kakao_id)
        return user

    def generate_jwt(self, user_id):
        return jwt.encode({
            'sub':user_id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, settings.SECRET_KEY, settings.ALGORITHM)

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