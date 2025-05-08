from django.db import models
from reservation.models import Reservation


class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[('payme', 'Payme'), ('Click', 'click')])
    approve_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'

