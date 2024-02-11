from datetime import timedelta, datetime
from django.conf import settings
from rest_framework import serializers
from .models import UserModel
import random



class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(
        write_only=True,
        min_length= settings.MIN_PASSWORD_LENGTH,
        error_messages={"min_length": f"Password must be longer than {settings.MIN_PASSWORD_LENGTH} characters."}
    )

    password2 = serializers.CharField(
        write_only=True,
        min_length= settings.MIN_PASSWORD_LENGTH,
        error_messages={"min_length": f"Password must be longer than {settings.MIN_PASSWORD_LENGTH} characters."}
    )

    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password1',
            'password2'
        )

    def validate(self, data):

        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password do not match.")

        return data
    

    def create(self, validated_data):

        # otp creation:
        otp = random.randint(100000, 999999)
        otp_expiry = datetime.now() + timedelta(minutes=10)
        
        user = UserModel(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY
        )

        user.set_password(validated_data['password1'])
        user.save()

        return user