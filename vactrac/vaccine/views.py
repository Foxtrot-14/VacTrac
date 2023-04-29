from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import *
from account.renderers import *
from rest_framework.permissions import IsAuthenticated
from .models import Vaccine
from .serializers import VaccineSerializer
# Create your views here.
class VaccineAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get(self, request):
        vaccine = Vaccine.objects.all()
        if vaccine is None:
            return Response({'msg':'No vaccines'}, status = status.HTTP_404_NOT_FOUND)
        serializer = VaccineSerializer(vaccine, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

class VaccineDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def get(self,pk, request):
        vaccine = Vaccine.objects.filter(pk=pk)
        if vaccine is None:
            return Response({'msg':'No vaccines found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = VaccineSerializer(vaccine, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)    