from django.urls import path

from spaces.views import SpaceListView, ReviewView, SpaceRegisterView

urlpatterns = [
    path('', SpaceListView.as_view()),
    path('/reviews', ReviewView.as_view()),
]