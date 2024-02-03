from rest_framework.decorators import api_view
from .serializers import RegistrationSerializers
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status
@api_view(['POST'])
@login_required
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    print("SS")
    if request.method == 'POST':
        serializer = RegistrationSerializers(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']="Registration Successfull"
            data['username']=account.username
            data['password']=account.password
            token=Token.objects.get(user=account).key
            data['token']=token
        else:
            data=serializer.errors
    return Response(data,status=status.HTTP_201_CREATED)
