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
from django.conf import settings
from tunanibackapp.views import LoginAPIView
from tunanibackapp.views import ListarPaqueteriasAPIView, CambiarPaqueteriaAPIView,VentasPorCooperativaAPIView,AgregarFotoCooperativaAPIView,CancelarVentaAPIView,CooperativaPaqueteriaAPIView, get_product_images,AgregarFotosAPIView,RegistroUsuarioAPIView,UsuarioRepresentanteDetalle,CooperativaView,ActualizarArtesanoAPIView,ListaCooperativasAPIView,CrearProductoAPIView,AgregarArtesanoAPIView, EliminarArtesanoAPIView,ListaArtesanosAPIView, ModificarProductoAPIView, BorrarProductoAPIView, AgregarFotosAPIView,ListaProductosAPIView
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/registro/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),
    path('api/productos/', ListaProductosAPIView.as_view(), name='lista_productos'),
    path('api/productos/crear/', CrearProductoAPIView.as_view(), name='crear_producto'),
    path('api/productos/modificar/<int:pk>/', ModificarProductoAPIView.as_view(), name='modificar_producto'),
    path('api/productos/borrar/<int:pk>/', BorrarProductoAPIView.as_view(), name='borrar_producto'),
    path('api/productos/<int:producto_id>/agregar-fotos/', AgregarFotosAPIView.as_view(), name='agregar_fotos_producto'),
    path('api/artesanos/', ListaArtesanosAPIView.as_view(), name='lista_artesanos'),
    path('api/artesanos/actualizar/<int:pk>/', ActualizarArtesanoAPIView.as_view(), name='actualizar_artesano'),
    path('api/artesanos/agregar/', AgregarArtesanoAPIView.as_view(), name='agregar_artesano'),
    path('api/artesanos/eliminar/<int:pk>/', EliminarArtesanoAPIView.as_view(), name='eliminar_artesano'),
    path('api/cooperativas/', ListaCooperativasAPIView.as_view(), name='lista-cooperativas'),
    path('api/cooperativa/<int:usuario_id>/', CooperativaView.as_view(), name='cooperativa_por_usuario'),
    path('api/usuario/representante/<int:pk>/', UsuarioRepresentanteDetalle.as_view(), name='detalle-usuario-representante'),
    path('api/subir-foto/', AgregarFotosAPIView.as_view(), name='subir_foto'),
    path('api/subir-foto-cooperativa/<int:pk>/', AgregarFotoCooperativaAPIView.as_view(), name='subir_foto'),
    path('api/producto/<int:producto_id>/imagenes/', get_product_images, name='producto_imagenes'),
    path('api/cooperativas/<int:cooperativa_id>/paqueteria/<int:paqueteria_id>/', CooperativaPaqueteriaAPIView.as_view(), name='paqueteria-detail'),
    path('api/cooperativas/<int:cooperativa_id>/paqueteria/', CooperativaPaqueteriaAPIView.as_view(), name='cooperativa-paqueteria'),
    path('api/cooperativas/<int:cooperativa_id>/ventas/', VentasPorCooperativaAPIView.as_view(), name='ventas_por_cooperativa'),
    path('api/ventas/<int:venta_id>/cancelar/', CancelarVentaAPIView.as_view(), name='cancelar-venta'),
    path('api/paqueterias/', ListarPaqueteriasAPIView.as_view(), name='listar-paqueterias'),
    path('api/cooperativas/<int:cooperativa_id>/cambiar-paqueteria/', CambiarPaqueteriaAPIView.as_view(), name='cambiar-paqueteria'),    
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
