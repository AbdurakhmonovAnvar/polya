from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            if not User.objects.filter(phone_number='+998900000101').exists():
                User.objects.create_superuser(
                    phone_number='+998900000101',
                    password='admin1234',
                    role='admin'
                )
        except (OperationalError, ObjectDoesNotExist, ProgrammingError):
            pass
