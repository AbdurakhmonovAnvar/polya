from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Region, Street
from django.conf import settings
import os
import json


@receiver(post_migrate)
def create_default_regions(sender, **kwargs):
    if Region.objects.exists():
        return  # allaqachon bor bo‘lsa, qaytib ket

    file_path = os.path.join(settings.BASE_DIR, 'regions.json')

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)

        for item in data:
            Region.objects.create(name=item['name_uz'])

        print("✅ Default regionlar muvaffaqiyatli qo‘shildi.")
        file_district = os.path.join(settings.BASE_DIR, 'districts.json')

        with open(file_district, 'r', encoding='utf-8-sig') as f_dist:
            data_dist = json.load(f_dist)
        for i in data_dist:
            for j in data:
                if i['region_id'] == j['id']:
                    region = Region.objects.get(name=j['name_uz'])
                    Street.objects.create(name=i['name_uz'], region=region)
        print("✅ Default district muvaffaqiyatli qo‘shildi.")

    except Exception as e:
        print(f"⚠️ Regionlarni yuklashda xatolik: {e}")

#ass