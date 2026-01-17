"""
Modelo Django para Cliente
NOTA: Esta es la capa de infraestructura, separada del dominio
"""
# from django.db import models
# from django.contrib.postgres.fields import UUIDField

# class ClienteModel(models.Model):
#     """
#     Modelo ORM para Cliente.
#     Mapea la entidad de dominio a la base de datos.
#     """
#     id = models.UUIDField(primary_key=True)
#     nombre = models.CharField(max_length=100)
#     apellido = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     tipo_documento = models.CharField(max_length=20)
#     numero_documento = models.CharField(max_length=50, unique=True)
#     telefono = models.CharField(max_length=20, null=True, blank=True)
#     activo = models.BooleanField(default=True)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)
#     
#     class Meta:
#         db_table = 'clientes'
#         verbose_name = 'Cliente'
#         verbose_name_plural = 'Clientes'
#         ordering = ['-fecha_creacion']

# Punto de extensión: implementar cuando se configure Django
