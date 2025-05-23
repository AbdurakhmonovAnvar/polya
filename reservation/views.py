from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateReservationSerializer, GetMyReservationsSerializers, GetAllReservationSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Reservation
from post.models import Polya


class CreateReservation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, polya_id):
        serializer = CreateReservationSerializer(data=request.data)

        # Polya tekshiruv
        try:
            polya = Polya.objects.get(pk=polya_id)
        except Polya.DoesNotExist:
            return Response({'message': 'Bunday polya topilmadi!'}, status=status.HTTP_404_NOT_FOUND)

        # Ma'lumot to'g'riligi tekshiriladi
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_time = serializer.validated_data.get('start_time')

        # Belgilangan vaqtga rezervatsiya mavjudmi?
        if Reservation.objects.filter(start_time=start_time, polya=polya).exists():
            return Response({'message': 'Bu vaqtda bron qilingan!'}, status=status.HTTP_400_BAD_REQUEST)

        # Saqlash
        serializer.save(customer=request.user, polya=polya)
        return Response({'message': 'Reservation saqlandi!'}, status=status.HTTP_201_CREATED)


class GetMyReservation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            reservation = Reservation.objects.get(customer=request.user)
        except Reservation.DoesNotExist:
            return Response({'message': 'Bu userda zakaslar yoq'})
        serializers = GetMyReservationsSerializers(reservation)
        return Response(serializers.data, status=status.HTTP_200_OK)


class GetAllReservation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservation = Reservation.objects.all()
        serializer = GetAllReservationSerializers(reservation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
