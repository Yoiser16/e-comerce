import os, sys
sys.path.insert(0, '/var/www/kharis-store/src')
os.environ['DJANGO_SETTINGS_MODULE'] = 'infrastructure.config.settings'

import django
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
        cursor.execute(
            "SELECT COUNT(*) FROM {} WHERE {} LIKE '%%localhost%%'".format(table, column)
        )
        count = cursor.fetchone()[0]
        print("{}.{}: {} rows with localhost".format(table, column, count))
        
        if count > 0:
            cursor.execute(
                "SELECT id, {} FROM {} WHERE {} LIKE '%%localhost%%' LIMIT 3".format(column, table, column)
            )
            for row in cursor.fetchall():
                val = str(row[1])
                if len(val) > 80:
                    val = val[:80] + "..."
                print("  BEFORE: " + val)
            
            cursor.execute(
                "UPDATE {} SET {} = REPLACE({}, 'http://localhost:8000', '') WHERE {} LIKE '%%localhost:8000%%'".format(table, column, column, column)
            )
            print("  Fixed {} rows".format(cursor.rowcount))
            
            cursor.execute(
                "UPDATE {} SET {} = REPLACE({}, 'http://localhost', '') WHERE {} LIKE '%%localhost%%'".format(table, column, column, column)
            )
            if cursor.rowcount > 0:
                print("  Fixed {} more rows (other ports)".format(cursor.rowcount))

    # Verify
    print("\n--- Verification ---")
    for table, column in tables_columns:
        cursor.execute(
            "SELECT COUNT(*) FROM {} WHERE {} LIKE '%%localhost%%'".format(table, column)
        )
        count = cursor.fetchone()[0]
        print("{}.{}: {} remaining".format(table, column, count))

print("\nDone!")
