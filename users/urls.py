from django.urls import path
from .views import SocialSignIn,ReservationView

urlpatterns = [
    path('/signin',SocialSignIn.as_view()),
    path('/reservation',ReservationView.as_view()),
]