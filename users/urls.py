from django.urls import path

from users.views import KaKaoSigninView, HostConvertView

urlpatterns = [
    path('/signin/kakao', KaKaoSigninView.as_view()),
    path('/host', HostConvertView.as_view()),
]