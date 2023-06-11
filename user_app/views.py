# from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import Users
# from django.views.decorators.csrf import csrf_exempt
from .serializers import SigninSirializer
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
# from django.shortcuts import redirect, render
from django.contrib import messages
from .UserSerializer import UserSerializer
import jwt
from rest_framework.exceptions import AuthenticationFailed
from dropbox.settings import SECRET_KEY

def login_view(request):
        if request.method == 'POST' :
            data = JSONParser().parse(request) # password = request.data['password']
            tokenData = SigninSirializer.validate(data)
            if type(tokenData) is JsonResponse:
                return tokenData
            email = data['email']
            user = Users.objects.get(email = email)
            SigninSirializer.update(user, tokenData)

            email = data['email']
            user = Users.objects.get(email = email)
            SigninSirializer.update(user, tokenData)

            response = JsonResponse({
                'user' : str(tokenData['user']),
                'access_token' : tokenData['access_token'],
                'refresh_token': tokenData['refresh_token']
            })

            return response
        
        return JsonResponse({
            "ResponseCode":403,
            "message":"http error"
        })
  


def logout(request):
    user = checkUser(request)
    Users.objects.filter(id = user.id).update(token = "")

    if request.method == 'POST':

        response = JsonResponse({
            "ResponseCode":200,
            "message" : "success"
        })
    else:
         response = JsonResponse({
             "ResponseCode":400,
            "message" : "error"
         })
    return response


def signup(request):
    # POST 요청으로 JSON 객체 받아오면
    if request.method == "POST":
        # 데이터 파싱 + 값 가져오기
        data = JSONParser().parse(request)

        # print(data)

        serializer = UserSerializer(data=data)

        # print(serializer.is_valid())
        # print(serializer.errors)
        # print(serializer.validated_data)

        if serializer.is_valid() :

            input_email = data['email'] # 입력된 email

            if Users.objects.filter(email = input_email).exists() : # 해당 email로 회원 조회
                # 존재하면 중복 id HTTP응답
                response = JsonResponse({
                    "ResponseCode":400,
                    "description" : "중복 id"

                }, status=400)

                return HttpResponse(status=400)

            elif '@' not in input_email or '.' not in input_email : # 형식이 맞지 않는 경우
                # 실패 HTTP응답
                response = JsonResponse({
                    "ResponseCode":400,
                    "description" : "형식이 맞지 않음"
                })
                return HttpResponse(status=400)

            else :
                serializer.save()
                response = JsonResponse({
                    "ResponseCode":200
                })
            return response
        
        else :
            response = JsonResponse({
                    "ResponseCode":400,
                    "description" : "형식이 맞지 않음"
                })
            return HttpResponse(status=400)
            

def modify(request):
    # validated = serializer.validated_data
    # instance = serializer.create(validated_data=validated)
    # print(instance)
    return 0


def checkUser(request):
    user_token = request.headers.get("Authorization", None).split(" ")[1]
    print(user_token)
    payload_data = decode_jwt_token(user_token)
    user = Users.objects.get(id= payload_data['user_id'])
    return user

# 토큰에서 payload 추출
def decode_jwt_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, 'HS256')
    #     return payload
    # except jwt.ExpiredSignatureError:
    #     raise AuthenticationFailed('Token expired')
    # except jwt.InvalidTokenError:
    #     raise AuthenticationFailed('Invalid token')

