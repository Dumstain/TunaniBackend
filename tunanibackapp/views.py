from django.shortcuts import render

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
    
    
