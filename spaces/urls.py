from django.urls import path

from spaces.views import SpaceListView, ReviewView

urlpatterns = [
    path('/lists', SpaceListView.as_view()),
    path('/reviews', ReviewView.as_view()),
]