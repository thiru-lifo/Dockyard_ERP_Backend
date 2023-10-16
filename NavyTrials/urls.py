"""ETMA URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from doctest import master
from django.contrib import admin
from django.urls import path, include
from NavyTrials import settings
from django.conf.urls.static import static
#from rest_framework import router
#from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


#router = DefaultRouter()
#router.register('countriesapi', viewset.CountriesViewset, basename = 'countriesapi')

urlpatterns = [

    #path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),
    path('notification/', include('notification.urls')),
    path('export/', include('export.urls')),
    path('api/auth/', include('authentication.urls')),
    # path('api-auth', include('rest_framework.urls')),
    # path('api/auth/token', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh', TokenRefreshView.as_view()),
    path('api/auth/token/verify', TokenVerifyView.as_view()),
    path('access/', include('access.urls')),
    path('configuration/', include('configuration.urls')),
    path ('log/',include('log.urls')),
    path ('transaction/',include('transaction.urls')),
    path ('restservice/', include('restservice.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
