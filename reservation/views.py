from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateReservationSerializer, GetMyReservationsSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Reservation
from post.models import Polya


class CreateReservation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, polya_id):
        serializer = CreateReservationSerializer(data=request.data)
        try:
            polya = Polya.objects.get(pk=polya_id)
        except Polya.DoesNotExist:
            return Response({'message': 'Bunday polya topilmadi!'})
        reservation = Reservation.objects.get(start_time=request.data.get('start_time'))
        if reservation:
            return Response({'message': 'Bu vaqtda bron qilingan'}, status=status.HTTP_400_BAD_REQUEST)
        if polya is None:
            return Response({'message': 'Bunday polya yoq'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(customer=request.user, polya=polya)
            return Response({'message': 'reservation saqlandi!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMyReservation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            reservation = Reservation.objects.get(customer=request.user)
        except Reservation.DoesNotExist:
            return Response({'message': 'Bu userda zakaslar yoq'})
        serializers = GetMyReservationsSerializers(reservation)
        return Response(serializers.data, status=status.HTTP_200_OK)
