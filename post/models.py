from django.db import models
from user.models import User


class Polya(models.Model):
    address = models.CharField(max_length=255, null=False)
    locations = models.TextField()
    images_path = models.TextField(blank=True)
    type = models.CharField(max_length=30, choices=[('Futsal', 'futsal'), ('Lawn', 'lawn')], default='Lawn')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polya_created')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    craeted_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'polya'


class Region(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'region'


class Street(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        db_table = 'street'

# ass