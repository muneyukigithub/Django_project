from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, SmallTask, CustomUser
from .serialyzer import (
    TaskSerializer,
    SmallTaskSerializer,
    UserSerializer,
    RegisterUserSerializer,
)
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
import jwt
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieHandlerJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

# from rest_framework.generics import

# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SmallTaskViewSet(viewsets.ModelViewSet):
    queryset = SmallTask.objects.all()
    serializer_class = SmallTaskSerializer


class fetchtest(APIView):
    # authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        print(request.user)

        return Response("fetch OK", status=200)

    def post(self, request):

        return Response("fetch OK", status=200)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# ユーザー登録API
class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        # print(request.data)
       
        # requestdata = {'email': 'admin@admin.com', 'password': 'password'}
        # test = {'staff': 0}

        # instance = get_object_or_404(CustomUser,email='admin@admin.com')
        # # instance= get_object_or_404(CustomUser,email='adminuser@admin.com')

        # newuser = RegisterUserSerializer(instance=instance,data=test,partial=True)
        # us = RegisterUserSerializer(instance)
        # # print(newuser.is_valid())
        # print(us.data)

        # if us.is_valid():
        #     print(us)
            # print(newuser.is_valid())
            # print(newuser.validated_data)
            # newuser.save()



        # u = CustomUser(**newuser.validated_data)
        # print(newuser.is_active())
        # print(u)

        # newuser = RegisterUserSerializer(data=request.data)

        try:
            newuser = RegisterUserSerializer(data=request.data)
            if newuser.is_valid():
                print("is_valid()")
                result = newuser.save()
        except:
            Response({"message": "error"}, 400)

        res = Response({"message":"error"}, status=200)
        try:
            newtoken = TokenObtainPairSerializer(
            data=request.data
        )

            if newtoken.is_valid():

                res = Response(newtoken.validated_data, status=200)

                res.set_cookie(
                        "access_token",
                        newtoken.validated_data["access"],
                        max_age=60 * 60 * 24,
                        httponly=True,
                        samesite="None",
                        secure=True,
                    )
                res.set_cookie(
                        "refresh_token",
                        newtoken.validated_data["refresh"],
                        max_age=60 * 60 * 24 * 30,
                        httponly=True,
                        samesite="None",
                        secure=True,
                    )
        except:
            pass

        return res


# Token発行API
class TokenObtainView(jwt_views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print(self.get_serializer)
        try:
            serializer = self.get_serializer(data=request.data)

        except:
            print("get_serializer error")
        # 検証
        try:
            serializer.is_valid(raise_exception=True)
        # エラーハンドリング
        except jwt_exp.TokenError as e:
            print("jwt_exp.TokenError")
            raise jwt_exp.InvalidToken(e.args[0])

        res = Response(serializer.validated_data, status=200)

        # try:
        #     res.delete_cookie("access_token")
        # except Exception as e:
        #     print("delete_cookie")
        #     print(e)

        # CookieヘッダーにTokenをセットする
        res.set_cookie(
            "access_token",
            serializer.validated_data["access"],
            max_age=60 * 60 * 24,
            httponly=True,
            samesite="None",
            secure=True,
        )
        res.set_cookie(
            "refresh_token",
            serializer.validated_data["refresh"],
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            samesite="None",
            secure=True,
        )

        # 最終的にはaccess_tokenとrefresh_tokenを返してもらう
        return res


# TokenからUser取得するAPI
class UserAPIView(APIView):
    def get_object(self, JWT):
        try:
            payload = jwt.decode(jwt=JWT, key=settings.SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(id=payload["user_id"])
            return user

        except Exception as e:
            print(e)

    def get(self, request, format=None):
        JWT = request.COOKIES.get("access_token")
        if not JWT:
            return Response({"error": "No token"}, status=400)

        user = self.get_object(JWT)
        serial = UserSerializer(user)
        # return Response({"error": "No token"}, status=200)

        return Response({"username": serial.data["email"]}, status=200)

    # RefreshToken取得API


def refresh_get(request):

    try:
        rt = request.COOKIES["refresh_token"]
        return JsonResponse({"refresh": rt}, safe=False)
    except Exception as e:
        print(e)

    return None

    # RefreshToken取得API


import json


class TokenRefresh(jwt_views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        print("---------request.data")
        print(request.data)
        print(type(request.data))
        nowtoken = {"refresh": request.COOKIES["refresh_token"]}
        print(type(nowtoken))
        print(json.dumps(nowtoken))
        # serializer = self.get_serializer(data=request.data)
        serializer = self.get_serializer(data=nowtoken)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])
        # token更新
        res = Response(serializer.validated_data, status=200)
        # 既存のAccess_Tokenを削除
        res.delete_cookie("access_token")
        # 更新したTokenをセット
        res.set_cookie(
            "access_token",
            serializer.validated_data["access"],
            max_age=60 * 24 * 24 * 30,
            httponly=True,
            samesite="None",
            secure=True,
        )
        return res

    # Token削除API


class LogoutView(jwt_views.TokenObtainPairView):
    # authentication_classes = (CookieHandlerJWTAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        # try:
        #     serializer.is_valid(raise_exception=True)
        # except jwt_exp.TokenError as e:
        #     raise jwt_exp.InvalidToken(e.args[0])

        # print(serializer.validated_data["access"])
        return Response("o", 200)

    def get(self, request, *args, **kwargs):

        res = Response({"message": "logout"}, status=200)
        # res.delete_cookie("access_token")
        # res.delete_cookie("refresh_token")
        res.set_cookie(
            "access_token",
            "",
            max_age=0,
            httponly=True,
            samesite="None",
            secure=True,
        )
        res.set_cookie(
            "refresh_token",
            "",
            max_age=0,
            httponly=True,
            samesite="None",
            secure=True,
        )

        return res

    # def post(self,request,*args,**kwargs):
    #     return
    # serializer = self.get_serializer(data=request.data)

    # try:
    #     serializer.is_valid(raise_exception=True)
    # except Exception as e:

    # res = Response(serializer.vali)
