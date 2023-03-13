"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'checkins', views.CheckinViewSet)
router.register(r'movies', views.MovieViewSet)

# URLの全体設計
urlpatterns = [
    # 今回作成するアプリ「app_folder」にアクセスするURL
    path('theatre/', include('theatreCheckIn.urls')),
    # 管理サイトにアクセスするURL
    path('admin/', admin.site.urls),
    # 何もURLを指定しない場合（app_config/views.pyで、自動的に「app_folder」にアクセスするよう設定済み）
    path('', include('accounts.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]