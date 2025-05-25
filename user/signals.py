# user/signal.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(phone_number='+998900000101').exists():
        User.objects.create_superuser(
            phone_number='+998900000101',
            password='admin1234',
            role='admin'
        )
