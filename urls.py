from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from core.views import TicketViewSet,CommentViewSet,ArticleViewSet,home
router=DefaultRouter(); router.register('tickets',TicketViewSet); router.register('comments',CommentViewSet); router.register('articles',ArticleViewSet)
urlpatterns=[path('admin/',admin.site.urls),path('api/',include(router.urls)),path('api/token/',TokenObtainPairView.as_view()),path('api/token/refresh/',TokenRefreshView.as_view()),path('',home)]
