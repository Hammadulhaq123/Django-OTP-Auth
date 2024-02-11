from rest_framework import viewsets

from .models import UserModel
from .serializers import UserSerializer

# 3

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
import random
from datetime import datetime, timedelta




class UserViewset(viewsets.ModelViewSet):

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()

        if(request.data.get('otp').length == 0):
            return Response("OTP cannot be left empty", status=status.HTTP_400_BAD_REQUEST)
        
        elif(request.data.get('otp').length < instance.otp):
            return Response("Otp doen't match minimum length criteria", status=status.HTTP_400_BAD_REQUEST)
        
        elif(request.data.get('otp') != instance.otp):
            return Response("Invalid OTP", status=status.HTTP_406_NOT_ACCEPTABLE)

        elif (
            not instance.is_active
            and instance.otp == request.data.get('otp')
            and instance.otp_expiry
            and timezone.now() < instance.otp_expiry
        ): 
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()

            return Response("Successfully verified the user.", status=status.HTTP_200_OK)
        

        return Response("User already active", status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        instance = self.get_object()

        if int(instance.max_otp_try == 0) and timezone.now() < instance.otp_max_out:
            return Response(
                "You've reached otp try limit. Please try again after an hour",
                status=status.HTTP_400_BAD_REQUEST
            )
        

        # otp regenration:
        otp = random.randint(100000, 999999)
        otp_expiry = datetime.now() + timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try ) - 1


        instance.otp = otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try

        if max_otp_try == 0:
            instance.otp_max_out = timezone.now() + timedelta(hours=1)

        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY

        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        
        instance.save()
        return Response("Otp Successfully regenerated", status=status.HTTP_200_OK)

        