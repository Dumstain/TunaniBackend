from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Token  # Asegúrate de importar el modelo Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario, Token
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FotoSerializer
from .serializers import ArtesanoSerializer
from .models import Artesano
from .models import Cooperativa
from .serializers import CooperativaSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Cooperativa, Paqueteria
from .serializers import PaqueteriaSerializer
from .serializers import VentaSerializer
from .models import Venta

class PedidosEnProcesoAPIView(APIView):
    def get(self, request, cooperativa_id):
        pedidos = Venta.objects.filter(cooperativa_id=cooperativa_id, estado='en_proceso')
        serializer = VentaSerializer(pedidos, many=True)
        return Response(serializer.data)


class CooperativaPaqueteriaAPIView(APIView):
    def get(self, request, cooperativa_id):
        try:
            cooperativa = Cooperativa.objects.get(pk=cooperativa_id)
            paqueteria = cooperativa.paqueteria
            serializer = PaqueteriaSerializer(paqueteria)
            return Response(serializer.data)
        except Cooperativa.DoesNotExist:
            return Response({'error': 'Cooperativa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Paqueteria.DoesNotExist:
            return Response({'error': 'Paqueteria no encontrada para la cooperativa especificada'}, status=status.HTTP_404_NOT_FOUND)

class AgregarFotosAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, producto_id):
        producto = get_object_or_404(Producto, pk=producto_id)
        fotos = request.FILES.getlist('imagen')
        for foto in fotos:
            foto_serializer = FotoSerializer(data={'ubicacion': foto, 'producto': producto.pk})
            if foto_serializer.is_valid():
                foto_serializer.save()
            else:
                return Response(foto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"mensaje": "Fotos agregadas correctamente al producto."}, status=status.HTTP_201_CREATED)


def get_product_images(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    fotos = producto.fotos.all()
    images_urls = [request.build_absolute_uri(foto.ubicacion.url) for foto in fotos if foto.ubicacion]
    return JsonResponse({'images': images_urls})
        
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        contrasenia = request.data.get('contrasenia')
        
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({"message": "Email inválido"}, status=status.HTTP_404_NOT_FOUND)
        
        if not check_password(contrasenia, usuario.contrasenia):
            return Response({"message": "Contraseña inválida"}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(usuario=usuario)

        # Aquí incluimos los datos adicionales en la respuesta
        respuesta = {
            "token": str(token.token),
            "usuario": usuario.nombre_user,
            "rol": usuario.rol.nombre_rol,  # Asegúrate de que tu modelo Rol tenga un campo 'nombre_rol'
            "id":usuario.id,
            "mensaje": f"Has sido logeado como {usuario.rol.nombre_rol}"
        }

        return Response(respuesta, status=status.HTTP_200_OK)


class RegistroUsuarioAPIView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            # Crear y guardar el token para el usuario
            Token.objects.create(usuario=usuario)
            return Response({"message": "Usuario registrado con éxito"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # Aquí puedes definir la política de permisos. Por defecto, solo superusuarios pueden hacer cualquier cosa.
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        # Aquí puedes añadir lógica adicional si es necesario antes de crear el usuario
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Aquí puedes añadir lógica adicional si es necesario antes de actualizar el usuario
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Aquí puedes añadir lógica adicional si es necesario antes de eliminar el usuario
        return super().destroy(request, *args, **kwargs)
    
    
class UsuarioRepresentanteDetalle(APIView):
    def get(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk, rol=2)  # Asumiendo que el rol 2 corresponde a representante
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'mensaje': 'El usuario representante no existe'}, status=status.HTTP_404_NOT_FOUND)   
    

class ListaArtesanosAPIView(APIView):
    def get(self, request):
        artesanos = Artesano.objects.all()
        serializer = ArtesanoSerializer(artesanos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AgregarArtesanoAPIView(APIView):
    def post(self, request):
        serializer = ArtesanoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EliminarArtesanoAPIView(APIView):
    
    # Eliminar un artesano específico
    def delete(self, request, pk):
        try:
            artesano = Artesano.objects.get(pk=pk)
            artesano.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Artesano.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class ActualizarArtesanoAPIView(APIView):
    def put(self, request, pk):
        try:
            artesano = Artesano.objects.get(pk=pk)
        except Artesano.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ArtesanoSerializer(artesano, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListaCooperativasAPIView(APIView):
    """
    Lista todas las cooperativas.
    """
    def get(self, request, format=None):
        cooperativas = Cooperativa.objects.all()
        serializer = CooperativaSerializer(cooperativas, many=True)
        return Response(serializer.data)
    
    
class CooperativaView(APIView):
    def get(self, request, usuario_id):
        try:
            cooperativa = Cooperativa.objects.get(usuario=usuario_id)
            serializer = CooperativaSerializer(cooperativa)
            return Response(serializer.data)
        except Cooperativa.DoesNotExist:
            return Response({'error': 'No se encontró la cooperativa asociada al usuario'}, status=status.HTTP_404_NOT_FOUND)
    
    
class ListaProductosAPIView(APIView):
    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
class CrearProductoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)  # Agrega esto para ver qué datos están llegando
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Esto mostrará los errores de validación
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModificarProductoAPIView(APIView):
    def put(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrarProductoAPIView(APIView):
    def delete(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AgregarFotosAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, producto_id):
        # Verifica que el Producto exista
        producto = get_object_or_404(Producto, pk=producto_id)
        
        # Crea una instancia de Foto para cada imagen subida y la asocia al producto
        fotos = request.FILES.getlist('imagen')  # Asegúrate de que el nombre del campo en el formulario sea 'imagen'
        for foto in fotos:
            foto_serializer = FotoSerializer(data={'imagen': foto, 'producto': producto.pk})
            if foto_serializer.is_valid():
                foto_serializer.save()
            else:
                return Response(foto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"mensaje": "Fotos agregadas correctamente al producto."}, status=status.HTTP_201_CREATED)
