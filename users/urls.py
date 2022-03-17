from django.urls import path
from .views      import SocialSignIn

urlpatterns = [
    path('/signin',SocialSignIn.as_view()),
]