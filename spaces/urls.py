from django.urls import path

from spaces.views import SpaceView, ReviewView, SpaceDetailView, BookingView, BookingListView

urlpatterns = [
    path('', SpaceView.as_view()),
    path('/reviews', ReviewView.as_view()),
    path('/detail/<int:space_id>', SpaceDetailView.as_view()),
    path('/<int:space_id>/booking', BookingView.as_view()),
    path('/bookinglist', BookingListView.as_view()),
]