from django.urls import path
from .views import SocialSignIn,ReservationView,ReservationHistoryView

urlpatterns = [
    path('/signin',SocialSignIn.as_view()),
    path('/reservation',ReservationView.as_view()),
    path('/mypage',ReservationHistoryView.as_view()),
]