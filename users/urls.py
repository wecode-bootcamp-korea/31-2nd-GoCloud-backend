from django.urls import path

from users.views import KakaoSigninView, HostConvertView

urlpatterns = [
    path('/signin/kakao', KakaoSigninView.as_view()),
    path('/host', HostConvertView.as_view()),
]