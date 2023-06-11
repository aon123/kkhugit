from .models import Users
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse 
from rest_framework import status
from django.contrib.auth.hashers import check_password

class SigninSirializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required = True,
        write_only = True
    )
    password = serializers.CharField(
        required = True,
        write_only = True,
        style= {'input_type' : 'password'}
    )
    token = serializers.CharField(
        required = True,
        write_only = True,
    )
    class Meta(object):
        model = Users
        fields = ('email', 'password')

    def validate(data):
        # email = data.get('email',None)
        # password = data.get('password',None)
        email = data['email']
        password = data['password']

        if Users.objects.filter(email=email).exists():
            user = Users.objects.get(email = email)

            if user.password != password: #not check_password(user.password ,password)->암호화
                return JsonResponse({
                    "Response Code": status.HTTP_404_NOT_FOUND,
                    "message": 'Check Your Email or Password'
                })
        
        else:
            return JsonResponse({
                    "Response Code": status.HTTP_404_NOT_FOUND,
                    "message": 'User does not exist'
                })
        
        user = Users.objects.get(id=user.id)

        token = RefreshToken.for_user(user)
        data = {
            'user' : user,
            'refresh_token' : str(token),
            'access_token' : str(token.access_token)
        }
        return data
    
    def update(instance, validated_data):
        instance.token = validated_data.get('refresh_token', instance.token)
        
        instance.save()
        
    
