from django.urls import path

from .views import  KaKaoSignInView, KaKaoSignInCallBackView

urlpatterns = [
    path('/signin/kakao', KaKaoSignInView.as_view()),
    path('/token', KaKaoSignInCallBackView.as_view())
]
