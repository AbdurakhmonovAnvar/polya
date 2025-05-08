from django.urls import path
from .views import CreateReservation, GetMyReservation

urlpatterns = [
    path('api/reservation/create/<int:polya_id>', CreateReservation.as_view(), name='reservation-create'),
    path('api/reservation/get-my-reservation', GetMyReservation.as_view(), name='my-reservation'),
]

