from xml.dom import ValidationErr
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['phone','name','type','password','password2','otp']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError('Passwords do not match') 
        return attrs  
      
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class OtpVerificationSerializer(serializers.Serializer):
    otp = serializers.IntegerField(write_only=True)
    class Meta:
        model = User
        fields = ['otp','is_verified']
    def validate(self, attrs):
        otp = attrs.get('otp')
        user = self.context.get('user')
        if user.otp != otp:
            raise serializers.ValidationError('Invalid OTP')
        user.is_verified = True
        user.save()
        return attrs      
    
class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    class Meta:
        model = User
        fields = ['phone','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        user.set_password(password)
        user.save() 
        return attrs    
    
class PasswordResetPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()
    class Meta:
        fields = ['phone']
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        if User.objects.filter(phone=phone).exists():
            user = User.objects.get(phone=phone)
            #encoding the uid to makesure it is not displayed in the url
            #encoding function takes bytes input so using force bytescto convert
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            #go to settings.py to change the amount of time this token is valid line 169
            link = 'http://localhost:3000/user/reset/'+uid+'/'+token
            '''this is a dummy link that will be sent through email, this link should point to a page where the user can input new password''' 
            print(link)
        else:
            raise ValidationErr('You are not a Registered User')
        return attrs

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=225, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']
        
    def validate(self,attrs):
        #exception handling so that the api is not hit pointlessly
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Passwords do not match')
            id = smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr('Token Invalid or Expired')
            user.set_password(password)
            user.save() 
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('Token Invalid or Expired') 
                                                 