"""
Script to fix localhost URLs stored in the database.
Strips http://localhost:8000 prefix from all image URL fields,
leaving only the relative path (e.g., /static/uploads/productos/...).

Run on VPS: python manage.py shell < scripts/fix_localhost_urls.py
"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.settings')
django.setup()

from django.db import connection

tables_columns = [
    ('productos', 'imagen_principal'),
    ('productos_variantes', 'imagen_url'),
    ('imagenes_producto', 'url'),
    ('categorias', 'imagen'),
]

with connection.cursor() as cursor:
    for table, column in tables_columns:
        # Count affected rows
        cursor.execute(
            f"SELECT COUNT(*) FROM {table} WHERE {column} LIKE %s",
            ['%localhost%']
        )
        count = cursor.fetchone()[0]
        print(f"\n[{table}.{column}] Found {count} rows with localhost URLs")
        
        if count > 0:
            # Show examples before fix
            cursor.execute(
                f"SELECT id, {column} FROM {table} WHERE {column} LIKE %s LIMIT 5",
                ['%localhost%']
            )
            rows = cursor.fetchall()
            for row in rows:
                print(f"  BEFORE: {row[0]} -> {row[1]}")
            
            # Fix: strip http://localhost:8000 and http://localhost prefix
            cursor.execute(
                f"UPDATE {table} SET {column} = REPLACE({column}, 'http://localhost:8000', '') WHERE {column} LIKE %s",
                ['%localhost:8000%']
            )
            fixed_8000 = cursor.rowcount
            
            cursor.execute(
                f"UPDATE {table} SET {column} = REPLACE({column}, 'http://localhost', '') WHERE {column} LIKE %s",
                ['%localhost%']
            )
            fixed_other = cursor.rowcount
            
            print(f"  FIXED: {fixed_8000} rows (port 8000) + {fixed_other} rows (other)")
            
            # Show examples after fix
            cursor.execute(
                f"SELECT id, {column} FROM {table} WHERE id IN ({','.join(['%s'] * len(rows))})",
                [r[0] for r in rows]
            )
            after_rows = cursor.fetchall()
            for row in after_rows:
                print(f"  AFTER:  {row[0]} -> {row[1]}")

print("\n✅ Done! All localhost URLs have been cleaned.")
