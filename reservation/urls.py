from django.urls import path
from .views import CreateReservation, GetMyReservation, GetAllReservation

urlpatterns = [
    path('api/create/<int:polya_id>', CreateReservation.as_view(), name='reservation-create'),
    path('api/get-my-reservation', GetMyReservation.as_view(), name='my-reservation'),
    path('api/get-all-reservation', GetAllReservation.as_view(), name='all-reservation'),
]
