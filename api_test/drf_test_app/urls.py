from django.urls import path, include
from .views import (
    # TaskViewSet,
    TaskView,
    SmallTaskView,
    # fetchtest,
    UserAPIView,
    TokenRefresh,
    refresh_get,
    LogoutView,
    UserRegisterView,
    UserDeactivate
)
from rest_framework import routers

# from rest_framework_simplejwt import views
from . import views

router = routers.DefaultRouter()
# task取得API
# router.register("task/", TaskViewSet)

# smalltask取得API
# router.register("smallTask/", SmallTaskViewSet)

# ユーザー登録API
# router.register("userRegist/",UserRegisterView.as_view())

# トークン取得API
# router.register("token/",views.TokenObtainView.as_view() )

# トークンリフレッシュAPI
# router.register("tokenRefresh/", TokenRefresh.as_view())

# リフレッシュトークン取得API
# router.register("refreshToken/", refresh_get)

# ログアウト
# router.register("logout/", LogoutView.as_view())

# ユーザー退会API
# router.register("userDeactivate", UserDeactivate.as_view())

# router.register("fetchTest", fetchtest)

urlpatterns = [

    # タスク取得API
    path("task/",TaskView.as_view(),name="task"),

    # スモールタスク取得API
    path("smalltask/",SmallTaskView.as_view(),name="task"),
    

    # ユーザー登録API
    path("userRegist/", UserRegisterView.as_view(), name="userRegist"),

    # トークン取得API
    path("token/",views.TokenObtainView.as_view(),name="TokenObtainView"),

    # トークンリフレッシュAPI
    path("tokenRefresh/", TokenRefresh.as_view(), name="TokenRefresh"),

    # リフレッシュトークン取得API
    path("refreshToken/", refresh_get,name="refreshToken"),

    # ユーザー情報取得API
    path("user/", UserAPIView.as_view(), name="UserAPIView"),

    # ログアウト
    path("logout/", LogoutView.as_view(), name="LogoutView"),

    # ユーザー退会API
    path("UserDeactivate/",UserDeactivate.as_view(),name="UserDeactivate"),   
    
   ]