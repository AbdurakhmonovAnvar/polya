from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from user.permissions import IsAdminRole, IsModeratorRole, IsAdminAndModeratorRole
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PolyaSerializer, PolyaUpdateSerializer, PolyaGetSerializer, GetAllPolyaSerializer, \
    GetPolyaByIdSerializer, GetMyLastReversationSerializer, GetStreetSerializers, GetRegionSerializers
from .models import Polya, Region, Street
import os
from uuid import uuid4
from django.conf import settings
from django.core.files.storage import default_storage
from user.models import User


class CreatePolya(APIView):
    permission_classes = [IsAuthenticated, IsAdminAndModeratorRole]

    def post(self, request):
        print(request.user.pk)
        address = request.data.get('address')
        locations = request.data.get('locations')
        owner_phone = request.data.get('owner_phone')
        street_name = request.data.get('street')
        region_name = request.data.get('region')
        owner_phone = request.data.get('owner_phone')
        type = request.data.get('type')
        region = Region.objects.get(name=region_name)
        if region is None:
            return Response({'message': "Region maydoni bo'sh"}, status=status.HTTP_404_NOT_FOUND)
        street = Street.objects.get(name=street_name)
        if street is None:
            return Response({'message': "Street maydoni bo'sh"}, status=status.HTTP_404_NOT_FOUND)
        if owner_phone is None:
            owner_phone = '0'
        status_value = request.data.get('status', True)
        images = request.FILES.getlist('images')  # Ko‘p rasm
        try:
            owner = User.objects.get(phone_number=owner_phone)
            polya = Polya.objects.create(
                address=address,
                locations=locations,
                status=status_value,
                creator=request.user,
                owner=owner,
                street=street,
                region=region,
                type=type
            )
        except User.DoesNotExist:
            polya = Polya.objects.create(
                address=address,
                locations=locations,
                status=status_value,
                creator=request.user,
                owner=request.user,
                region=region,
                street=street,
                type=type
            )

        image_urls = []

        # Har bir rasmni polya uchun alohida papkaga saqlaymiz
        polya_folder = f'polya_images/polya_{polya.id}'
        os.makedirs(os.path.join(settings.MEDIA_ROOT, polya_folder), exist_ok=True)

        for img in images:
            filename = f"{uuid4().hex}_{img.name}"
            path = os.path.join(polya_folder, filename)
            full_path = os.path.join(settings.MEDIA_ROOT, path)

            with default_storage.open(path, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)

            image_urls.append(f"{settings.MEDIA_URL}{path}")

        # Saqlangan URL’larni vergul bilan qo‘shamiz
        polya.image_url = ','.join(image_urls)
        polya.save()

        return Response({
            'message': 'Polya created successfully.',
            'polya_id': polya.id,
            'image_urls': image_urls
        }, status=status.HTTP_201_CREATED)


class UpdatePolya(APIView):
    permission_classes = [IsAuthenticated, IsAdminAndModeratorRole]

    def get_object(self, polya_id):
        try:
            return Polya.objects.get(pk=polya_id)
        except Polya.DoesNotExist:
            return None  # Faqat None qaytaramiz, Response emas

    def put(self, request, address):
        polya = self.get_object(address)

        if polya is None:
            return Response({"error": "Bunday addressli Polya topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PolyaUpdateSerializer(instance=polya, data=request.data, partial=True,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPolya(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        polya = Polya.objects.filter(owner=user)
        serializer = PolyaGetSerializer(polya, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllPolya(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        polya = Polya.objects.all()
        serializer = GetAllPolyaSerializer(polya, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPolyaById(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            polya = Polya.objects.get(pk=id)
        except Polya.DoesNotExist:
            return Response({'message': 'Polya topilmadi'})
        serializer = GetPolyaByIdSerializer(polya)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetRegions(APIView):
    def get(self, request):
        region = Region.objects.all()
        serializer = GetRegionSerializers(region, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStreet(APIView):
    def get(self, request, region_name):
        try:
            region = Region.objects.get(name=region_name)
        except Region.DoesNotExist:
            return Response({'message': 'Bunday region mavjud emas'}, status=status.HTTP_404_NOT_FOUND)

        streets = Street.objects.filter(region=region)
        serializer = GetStreetSerializers(streets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPolyaByRegionAndStreet(APIView):
    def get(self, request, region_name, street_name):
        try:
            region = Region.objects.get(name=region_name)
        except Region.DoesNotExist:
            return Response({'message': 'Region topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        try:
            street = Street.objects.get(name=street_name)
        except Street.DoesNotExist:
            return Response({'message': 'Street topilmadi'}, status=status.HTTP_404_NOT_FOUND)
        polya = Polya.objects.filter(region=region, street=street)
        if polya is None:
            return Response({'message': "Polyalar topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetAllPolyaSerializer(polya, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
