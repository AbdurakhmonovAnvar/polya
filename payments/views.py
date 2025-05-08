from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Payment
from reservation.models import Reservation
from .serializers import CreatePaymentSerializers, GetMyPaymentsSerializers, GetMyLastPaymentSerializers


class CreatePayment(APIView):
    permission_classes = IsAuthenticated

    def post(self, request, reservation_id):
        serializers = CreatePaymentSerializers(data=request.data)
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            return Response({'message': 'bunday order yoq'}, status=status.HTTP_400_BAD_REQUEST)
        if serializers.is_valid():
            serializers.save(reservation=reservation,approve_status=True)
            reservation.status = True
            reservation.save()
            return Response({'message': 'payment saqlandi'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMyPayments(APIView):
    permission_classes = IsAuthenticated

    def get(self, request):
        try:
            reservation = Reservation.objects.all(customer=request.user)
        except Reservation.DoesNotExist:
            return Response({'message': 'Bunday user yoq'}, status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.all(reservation=reservation)
        serializers = GetMyPaymentsSerializers(payment, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class GetMyLastPayment(APIView):
    permission_classes = IsAuthenticated

    def get(self, request):
        try:
            reservation = Reservation.objects.all(customer=request.user)
        except Reservation.DoesNotExist:
            return Response({'message': 'Bunday user yoq'}, status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.latest('created_at')
        serializers = GetMyPaymentsSerializers(payment)
        return Response(serializers.data, status=status.HTTP_200_OK)
