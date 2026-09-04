from django.urls import path
from shop import views

urlpatterns = [
    path('login/', views.MemberLoginView.as_view()),
    path('register/', views.MemberRegisterView.as_view()),
    path('banner/', views.BannerListView.as_view(), name='banner'),
]
