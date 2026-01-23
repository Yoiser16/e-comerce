import os
import sys
import django
from django.utils.text import slugify

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infrastructure.config.django_settings")
django.setup()

from infrastructure.persistence.django.models import CategoriaModel

def rename_category():
    old_name = "Cosméticos"
    new_name = "Accesorios"
    
    try:
        # Buscar la categoría por nombre exacto o aproximado
        categoria = CategoriaModel.objects.filter(nombre__icontains="Cosméticos").first()
        
        if not categoria:
            print(f"❌ Categoría '{old_name}' no encontrada.")
            # Listar categorías existentes para depuración
            print("Categorías disponibles:", list(CategoriaModel.objects.values_list('nombre', flat=True)))
            return

        print(f"✅ Categoría encontrada: {categoria.nombre} (Slug: {categoria.slug})")
        
        # Verificar si ya existe 'Accesorios'
        if CategoriaModel.objects.filter(nombre__iexact=new_name).exists():
            print(f"⚠️ La categoría target '{new_name}' ya existe.")
            target_cat = CategoriaModel.objects.get(nombre__iexact=new_name)
            # Mover productos? Por ahora solo avisar.
            print("No se realizó el cambio para evitar duplicados.")
            return

        # Renombrar
        categoria.nombre = new_name
        categoria.slug = slugify(new_name)
        categoria.save()
        
        print(f"🚀 Categoría renombrada exitosamente a: {categoria.nombre} (Slug: {categoria.slug})")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    rename_category()
