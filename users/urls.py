from django.urls import path

from users.views import KakaoSigninView, HostConvertView, WishListView, PostWishView

urlpatterns = [
    path('/signin/kakao', KakaoSigninView.as_view()),
    path('/host', HostConvertView.as_view()),
    path('/wishlist', WishListView.as_view()),
    path('/wish/<int:space_id>', PostWishView.as_view()),
]