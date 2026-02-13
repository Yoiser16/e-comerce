"""
Admin configuration for Cliente model
"""
from django.contrib import admin
from .models import ClienteModel, CategoriaModel, ResenaProductoModel


@admin.register(CategoriaModel)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'prioridad', 'orden', 'activo', 'mostrar_en_home', 'fecha_creacion')
    list_filter = ('activo', 'prioridad', 'mostrar_en_home')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('id', 'fecha_creacion', 'fecha_modificacion')
    ordering = ('prioridad', 'orden', 'nombre')
    prepopulated_fields = {'slug': ('nombre',)}
    
    fieldsets = (
        ('Información', {
            'fields': ('nombre', 'slug', 'descripcion', 'descripcion_corta')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
        ('Visualización', {
            'fields': ('prioridad', 'orden', 'mostrar_en_home')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Metadatos', {
            'fields': ('id', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ClienteModel)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'apellido', 'tipo_documento', 'numero_documento', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'tipo_documento', 'fecha_creacion')
    search_fields = ('nombre', 'apellido', 'email', 'numero_documento')
    readonly_fields = ('id', 'fecha_creacion', 'fecha_modificacion')
    ordering = ('-fecha_creacion',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'email')
        }),
        ('Documento de Identidad', {
            'fields': ('tipo_documento', 'numero_documento')
        }),
        ('Contacto', {
            'fields': ('telefono',)
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Metadatos', {
            'fields': ('id', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ResenaProductoModel)
class ResenaProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cliente', 'rating', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'rating', 'fecha_creacion')
    search_fields = ('producto__nombre', 'cliente__email', 'cliente__nombre', 'cliente__apellido')
    readonly_fields = ('id', 'fecha_creacion', 'fecha_modificacion')
    ordering = ('-fecha_creacion',)

    fieldsets = (
        ('Reseña', {
            'fields': ('producto', 'cliente', 'orden', 'rating', 'estado')
        }),
        ('Metadatos', {
            'fields': ('id', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
