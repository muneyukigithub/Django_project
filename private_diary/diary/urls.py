from django.urls import URLPattern, path
from . import views

app_name = 'diary'
urlpatterns = [
    path("",views.IndexView.as_view(),name="index"),
    path("form",views.InquiryView.as_view(),name="form"),
]