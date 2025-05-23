from django.db import models
from user.models import User
from post.models import Polya


class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    polya = models.ForeignKey(Polya, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=False)
    end_time = models.DateTimeField(auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    payments = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    class Meta:
        db_table = 'reservation'
