import json
from decimal import Decimal

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import MultiPartParser

class GetBanners(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

