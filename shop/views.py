from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from shop.models import Banner, Member
from shop.serializers import MemberCreateSerializer, MemberLoginSerializer, BannerSerializer


class MemberRegisterView(CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberCreateSerializer
    permission_classes = [permissions.AllowAny]


class MemberLoginView(TokenObtainPairView):
    queryset = User.objects.all()
    serializer_class = MemberLoginSerializer


class BannerListView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

