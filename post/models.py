from django.db import models
from user.models import User


class Polya(models.Model):
    address = models.CharField(max_length=255, null=False)
    locations = models.TextField()
    images_path = models.TextField(blank=True)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='polya_created')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    craeted_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'polya'


