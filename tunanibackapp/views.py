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
    
    
class CrearProductoAPIView(APIView):
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
