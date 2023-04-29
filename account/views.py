from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import *
from django.contrib.auth import authenticate
from account.renderers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
# Create your views here.

def get_tokens_for_user(user):
    #generating token manually
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class RegistrationView(APIView):
    #to server errors to the frontend
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        otp = random.randint(1000,9999)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(otp=otp)
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successfull'}, status=status.HTTP_201_CREATED)
    
class OtpVerificationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = OtpVerificationSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Phone Number Verified'}, status=status.HTTP_200_OK)
        
class LoginView(APIView):
    #to serve errors to the frontend
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.data.get('phone')
        password = serializer.data.get('password')
        user = authenticate(phone=phone,password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Logged In Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Phone Number or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class ProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    
class PasswordResetPhoneView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = PasswordResetPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link sent as sms check Phone'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,uid,token,format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)       
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
