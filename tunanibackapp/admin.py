# Register your models here.
from django.contrib import admin
from .models import Usuario, Rol, Datos, Cooperativa, Artesano, Producto, Venta, Comentario, DetalleVenta, Fotos


class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields = ('password',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
admin.site.register(Datos)
admin.site.register(Cooperativa)
admin.site.register(Artesano)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Comentario)
admin.site.register(DetalleVenta)
admin.site.register(Fotos)


