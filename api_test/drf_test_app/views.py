from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, SmallTask, CustomUser
from .serialyzer import (
    TaskSerializer,
    SmallTaskSerializer,
    UserSerializer,
    RegisterUserSerializer,
    DetailTaskSerializer
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
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from rest_framework.generics import

# Create your views here.


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

class SmallTaskView(APIView):
    def get(self,request):
        try:
            tasks = SmallTask.objects.all()
         
            # シリアライズする場合、
            serializer = SmallTaskSerializer(instance=tasks,many=True)

            return Response({"data":serializer.data,"type":"success"},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
        
        return Response({"type":"error"},status=status.HTTP_200_OK)

        
class TaskView(APIView):
    def get(self,request):
        try:
            # tasks = Task.objects.all()
            # serializer = TaskSerializer(instance=tasks,many=True)
            tasks = Task.objects.filter(created_at="2023-01-10")
            # serializer = TaskSerializer(instance=tasks,many=True)
            serializer = DetailTaskSerializer(instance=tasks,many=True)  
            return Response(serializer.data,status=status.HTTP_200_OK)

            # return Response({"data":serializer.data,"type":"success"},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
       
        return Response({"type":"error"},status=status.HTTP_200_OK)

    def post(self,request):

             
      
        # user = CustomUser(email=request.data["created_user"])
        # user = CustomUser.objects.get(data = newtask)

        savetask = ""
        for task in request.data:
            newtask = {"task":task["task"],"created_user":CustomUser.objects.get(email=task["created_user"]).id}
            serializer = TaskSerializer(data=newtask)
            if serializer.is_valid():
                savetask = serializer.save()
            # user_objects = []
            # print(request.data["smalltask"])
            for data in request.data:
                for _smalltask in data["smalltask"]:
                    print(_smalltask["smalltask"])
                    smalltask = {"smalltask":_smalltask["smalltask"],"task_id":savetask.task_id}
                    serializer = SmallTaskSerializer(data=smalltask)
                    if serializer.is_valid():
                        serializer.save()

        return Response({"type":"os"},status=status.HTTP_200_OK)
        
        


# class SmallTaskViewSet(viewsets.ModelViewSet):
#     queryset = SmallTask.objects.all()
#     serializer_class = SmallTaskSerializer

# ユーザー退会API
class UserDeactivate(APIView):
    def post(self, request, *args, **kwargs):
        try:
            instance = CustomUser.objects.get(email=request.data["email"])
            serializer = UserSerializer(instance=instance,data={"active":1},partial=True)

            if serializer.is_valid():
                username = serializer.save()
                print(username)
            return Response({"data":{"username":""},"type":"success"},status=status.HTTP_200_OK)

        except Exception as e:
            pass

        return Response({"data":"","type":"error"},status=status.HTTP_200_OK)

# ユーザー登録API
class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):

        # response = Response({"type":"error"},status=status.HTTP_200_OK)
        response = Response()

        try:
            
            newuser = RegisterUserSerializer(data=request.data)
            if newuser.is_valid():
                user = newuser.save()
                token = TokenObtainPairSerializer.get_token(user)
                response.set_cookie(
                        "access_token",
                        # newtoken.validated_data["access"],
                        str(token.access_token),
                        max_age=60 * 60 * 24,
                        httponly=True,
                        samesite="None",
                        secure=True,
                    )
                response.set_cookie(
                        "refresh_token",
                        # newtoken.validated_data["refresh"],
                        str(token),
                        max_age=60 * 60 * 24 * 30,
                        httponly=True,
                        samesite="None",
                        secure=True,
                    )

                response.data = {"type":"success","access_token":str(token.access_token),"refresh":str(token)}
                response.status_code = 200
                return response

        except Exception as e:
            print(e)


        return Response({"type":"error"},status=status.HTTP_400_BAD_REQUEST)


# Token発行API
class TokenObtainView(jwt_views.TokenObtainPairView):

    # def options(self, request):
    #     print("request")
    #     return Response()
    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            serializer = self.get_serializer(data=request.data)
            print(serializer)

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
