from django.apps import AppConfig


class ReservationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservation'

    def ready(self):
        # Ma'lumotlar bazasiga so'rov yubormaslik kerak
        pass



