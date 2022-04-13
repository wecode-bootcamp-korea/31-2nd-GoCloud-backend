from django.urls import path

from users.views import KaKaoSigninView

urlpatterns = [
    path('/signin/kakao', KaKaoSigninView.as_view()),
]