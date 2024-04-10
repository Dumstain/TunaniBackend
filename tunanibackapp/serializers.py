from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Datos, Usuario, Rol, Cooperativa, Artesano, Producto, Venta, Comentario, DetalleVenta, Fotos
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate
from rest_framework import exceptions
from .models import Producto
from .models import Fotos



User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    contrasenia = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['contrasenia'])
        if user is None:
            raise serializers.ValidationError("Credenciales inválidas")
        return user



class DatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datos
        fields = ['nombre', 'materno', 'paterno', 'tel', 'ine', 'metodo_pago', 'notificaciones']

class UsuarioSerializer(serializers.ModelSerializer):
    datos = DatosSerializer()
    
    class Meta:
        model = Usuario
        fields = ['nombre_user', 'email', 'contrasenia', 'rol', 'datos']
        extra_kwargs = {'contrasenia': {'write_only': True}}

    def create(self, validated_data):
        datos_data = validated_data.pop('datos')
        datos = Datos.objects.create(**datos_data)
        usuario = Usuario(**validated_data)
        
        try:
            usuario.rol = Rol.objects.get(id=3)  # Asumiendo que 3 es el ID para "comprador"
        except Rol.DoesNotExist:
            # Manejar el caso de que el rol no exista. Podrías crear el rol aquí o lanzar una excepción.
            raise serializers.ValidationError("Rol 'comprador' no encontrado.")
        
        usuario.contrasenia = make_password(usuario.contrasenia)
        usuario.datos = datos
        usuario.save()
        
        return usuario

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class CooperativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperativa
        fields = '__all__'

class ArtesanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artesano
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'


class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = ['imagen', 'producto']



class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'categoria', 'descripcion', 'material', 'stock', 'estado', 'artesano']
