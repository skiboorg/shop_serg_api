from django.urls import path,include
from . import views

urlpatterns = [
    path('banners', views.GetBanners.as_view()),





]
