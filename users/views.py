import requests

from django.http      import JsonResponse
from django.shortcuts import redirect
from django.views     import View

class KaKaoSignInView(View):
    def get(self, request):
        app_key      = '8a40225631e200c6fa438c1d08d5fdf6'
        redirect_uri = 'http://127.0.0.1:8000/users/signin/kakao/callback'

        return redirect(
            f'https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={app_key}&redirect_uri={redirect_uri}'
        )
    

class KaKaoSignInCallBackView(View):
    def get(self, request):
        app_key         = '8a40225631e200c6fa438c1d08d5fdf6'
        auth_code       = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'

        data = {
            'Content-type': 'application/x-www-form-urlencoded',
            'grant_type'  : 'authorization_code',
            'client_id'   : app_key,
            'code'        : auth_code
        }

        token = requests.post(kakao_token_api, data=data)

        return JsonResponse({'token' : token.json()}, status=200)
        
        
