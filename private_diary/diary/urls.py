from django.urls import URLPattern, path
from . import views

app_name = 'diary'
urlpattern = [
    path("",views.IndexView.as_view(),name="index"),
]