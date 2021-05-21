from django.urls import path
from .views import UserDirectMessageView

urlpatterns = [
    path("dm/<username>/", UserDirectMessageView.as_view())
]
