from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Datos, Usuario, Rol, Cooperativa, Artesano, Producto, Venta, Comentario, DetalleVenta, Fotos, Paqueteria
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, authenticate
from rest_framework import exceptions
from .models import Producto
from .models import Fotos, FotoCooperativa
from django.conf import settings
from .models import DetalleVenta



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
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class UsuarioSerializer(serializers.ModelSerializer):
    datos = DatosSerializer()
    
    class Meta:
        model = Usuario
        fields = ['nombre_user', 'email', 'contrasenia', 'rol', 'datos']
        extra_kwargs = {'contrasenia': {'write_only': True}}

    def create(self, validated_data):
        datos_data = validated_data.pop('datos')
        datos = Datos.objects.create(**datos_data)
        contrasenia = make_password(validated_data.pop('contrasenia'))
        
        usuario = Usuario(contrasenia=contrasenia, **validated_data)
        
        try:
            usuario.rol = Rol.objects.get(id=3)  # Asumiendo que 3 es el ID para "comprador"
        except Rol.DoesNotExist:
            raise serializers.ValidationError("Rol 'comprador' no encontrado.")
        
        usuario.datos = datos
        usuario.save()
        return usuario

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


from rest_framework import serializers

class CooperativaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Cooperativa
        fields = '__all__'  # Asegúrate de incluir 'imagen_url' si decides listar los campos explícitamente

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.foto and hasattr(obj.foto, 'ubicacion') and obj.foto.ubicacion:
            if request:
                return request.build_absolute_uri(obj.foto.ubicacion.url)
        return None


class ArtesanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artesano
        fields = '__all__'
        
class FotoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Fotos
        fields = ['id', 'ubicacion', 'imagen_url', 'producto']  # Añadir 'ubicacion' y 'producto' para manejar la carga

    def get_imagen_url(self, obj):
        if obj.ubicacion and hasattr(obj.ubicacion, 'url'):
            return obj.ubicacion.url
        return None

    def create(self, validated_data):
        # Aquí se crea la instancia de Fotos y se guarda, incluyendo el archivo de imagen y la relación con Producto
        return Fotos.objects.create(**validated_data)
    
class ProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'categoria', 'descripcion', 'material', 'stock', 'estado', 'artesano', 'fotos', 'imagen_url']

    def get_imagen_url(self, obj):
        # Solo devolver la URL de la imagen si el contexto lo requiere
        if self.context.get('show_imagen_url', False):
            request = self.context.get('request')
            if obj.fotos.exists():
                return request.build_absolute_uri(obj.fotos.first().ubicacion.url)
        return None


        
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()

    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(source='detalleventa_set', many=True)

    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'hora', 'precio_venta', 'gasto_envio', 'total_sn', 'subtotal', 'estado', 'numero_seguimiento', 'numero_pago', 'metodo_pago', 'cooperativa', 'detalles']


class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = ['id', 'ubicacion', 'producto']

    def create(self, validated_data):
        return Fotos.objects.create(**validated_data)

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.fotos.exists():  # Asegurando que el producto tiene al menos una foto
            return request.build_absolute_uri(obj.fotos.first().ubicacion.url)
        return None

class PaqueteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paqueteria
        fields = '__all__'
        
class FotoCooperativaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = FotoCooperativa
        fields = ['id', 'ubicacion', 'imagen_url', 'cooperativa']

    def get_imagen_url(self, obj):
        return obj.ubicacion.url if obj.ubicacion else None

    def create(self, validated_data):
        return FotoCooperativa.objects.create(**validated_data)

