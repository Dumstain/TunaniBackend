"""
URL configuration for tunaniback project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from tunanibackapp.views import LoginAPIView
from tunanibackapp.views import RegistroUsuarioAPIView,CrearProductoAPIView, ModificarProductoAPIView, BorrarProductoAPIView, AgregarFotosAPIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('registro/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),
    path('api/productos/crear/', CrearProductoAPIView.as_view(), name='crear_producto'),
    path('api/productos/modificar/<int:pk>/', ModificarProductoAPIView.as_view(), name='modificar_producto'),
    path('api/productos/borrar/<int:pk>/', BorrarProductoAPIView.as_view(), name='borrar_producto'),
    path('api/productos/<int:producto_id>/agregar-fotos/', AgregarFotosAPIView.as_view(), name='agregar_fotos_producto'),

]
