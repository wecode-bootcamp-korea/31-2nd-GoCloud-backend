from django.urls import path

from spaces.views import SpaceListView

urlpatterns = [
    path('', SpaceListView.as_view()),
]