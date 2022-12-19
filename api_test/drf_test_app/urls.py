from django.urls import path, include
from .views import (
    TaskViewSet,
    SmallTaskViewSet,
    fetchtest,
    UserAPIView,
    TokenRefresh,
    refresh_get,
)
from rest_framework import routers

# from rest_framework_simplejwt import views
from . import views

router = routers.DefaultRouter()
router.register("Task", TaskViewSet)
router.register("SmallTask", SmallTaskViewSet)
# router.register("fetchTest", fetchtest)

urlpatterns = [
    path("api/", include(router.urls)),
    # JWTトークン生成
    path("api/v1/token/", views.TokenObtainView.as_view(), name="token_obtain_pair"),
    # path("fetchTest/", fetchtest.as_view(), name="fetchTest"),
    path("user/", UserAPIView.as_view(), name="UserAPIView"),
    path("refresh/", TokenRefresh.as_view(), name="TokenRefresh"),
    path("refreshget/", refresh_get, name="Refreshget"),
]
