from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre_rol

class Datos(models.Model):
    nombre = models.CharField(max_length=45)
    materno = models.CharField(max_length=45)
    paterno = models.CharField(max_length=45)
    tel = models.CharField(max_length=10, blank=True, null=True)
    ine = models.CharField(max_length=45, blank=True, null=True)
    metodo_pago = models.CharField(max_length=45, blank=True, null=True)
    notificaciones = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.paterno} {self.materno}"

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre_user = models.CharField(max_length=45)
    contrasenia = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Necesario para acceder al admin

    datos = models.OneToOneField('Datos', on_delete=models.CASCADE, unique=True)
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE, related_name='usuarios')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    def __str__(self):
        return self.email
    def set_password(self, raw_password):
        self.contrasenia = raw_password
    
class Token(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='token')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)    

class Paqueteria(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    municipio = models.CharField(max_length=45)
    colonia = models.CharField(max_length=45, blank=True, null=True)
    calle = models.CharField(max_length=45, blank=True, null=True)
    num_ext = models.CharField(max_length=5, blank=True, null=True)
    tel = models.CharField(max_length=15)
    email = models.EmailField()
    servicio_ofrecido = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Cooperativa(models.Model):
    nombre = models.CharField(max_length=45)
    codigo_postal = models.CharField(max_length=45)
    cuenta_bancaria = models.CharField(max_length=45)
    descripcion = models.TextField(max_length=256, blank=True, null=True)
    rfc = models.CharField(max_length=15)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    paqueteria = models.ForeignKey(Paqueteria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Artesano(models.Model):
    nombre = models.CharField(max_length=45)
    apellido_materno = models.CharField(max_length=45)
    apellido_paterno = models.CharField(max_length=45)
    tel = models.CharField(max_length=45)
    email = models.EmailField(blank=True, null=True)
    rfc = models.CharField(max_length=45)
    ine = models.CharField(max_length=45, blank=True, null=True)
    numero_tarjeta = models.CharField(max_length=45)
    enfoque = models.TextField(max_length=256, blank=True, null=True)
    descripcion = models.TextField(max_length=256, blank=True, null=True)
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

class Producto(models.Model):
    # Opciones para el estado del producto
    ESTADO_OPCIONES = (
        ('publicado', 'Publicado'),
        ('no_publicado', 'No Publicado'),
    )

    nombre = models.CharField(max_length=45)
    precio = models.FloatField()
    categoria = models.CharField(max_length=45)
    descripcion = models.TextField(max_length=256, blank=True, null=True)
    material = models.CharField(max_length=45)
    stock = models.IntegerField()
    artesano = models.ForeignKey('Artesano', on_delete=models.CASCADE)
    estado = models.CharField(max_length=12, choices=ESTADO_OPCIONES, default='no_publicado')

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    precio_venta = models.FloatField(blank=True, null=True)
    gasto_envio = models.FloatField(blank=True, null=True)
    total_sn = models.FloatField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    numero_seguimiento = models.CharField(max_length=45, blank=True, null=True)
    numero_pago = models.CharField(max_length=45, blank=True, null=True)
    metodo_pago = models.CharField(max_length=45, blank=True, null=True)
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class Comentario(models.Model):
    comentario = models.TextField(max_length=255, blank=True, null=True)
    calificacion = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comentario {self.id} - {self.producto.nombre}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.FloatField()

    def __str__(self):
        return f"Detalle {self.id} - {self.venta.id}"

class Fotos(models.Model):
    ubicacion = models.ImageField(upload_to='imagenes_productos/', null=True, blank=True)
    producto = models.ForeignKey('Producto', related_name='fotos', on_delete=models.CASCADE)

    def __str__(self):
        if self.ubicacion and hasattr(self.ubicacion, 'url'):
            return self.ubicacion.url
        return "No image available"
    
class FotoCooperativa(models.Model):
    ubicacion = models.ImageField(upload_to='imagenes_cooperativas/', null=True, blank=True)
    cooperativa = models.OneToOneField('Cooperativa', related_name='foto', on_delete=models.CASCADE)

    def __str__(self):
        return self.ubicacion.url if self.ubicacion else "No image available"

    


