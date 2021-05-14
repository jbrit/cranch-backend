from django.urls import path
from .views import RegisterUserView

urlpatterns = [
    path("user/register/", RegisterUserView.as_view())
]
