#!/bin/bash
# Check for missing product image files
export PGPASSWORD='ecommerce_dev_2026!'
DB_USER="ecommerce_user"
DB_NAME="ecommerce_db"

echo "=== Checking missing image files ==="

# Check productos.imagen_principal
psql -U $DB_USER -d $DB_NAME -h localhost -t -A -c "SELECT imagen_principal FROM productos WHERE imagen_principal LIKE '/static/uploads/%'" | while IFS= read -r url; do
    url=$(echo "$url" | tr -d '[:space:]')
    if [ -n "$url" ]; then
        file="/var/www/kharis-store$url"
        if [ ! -f "$file" ]; then
            echo "MISSING (productos): $url"
        fi
    fi
done

# Check imagenes_producto.url
psql -U $DB_USER -d $DB_NAME -h localhost -t -A -c "SELECT url FROM imagenes_producto WHERE url LIKE '/static/uploads/%'" | while IFS= read -r url; do
    url=$(echo "$url" | tr -d '[:space:]')
    if [ -n "$url" ]; then
        file="/var/www/kharis-store$url"
        if [ ! -f "$file" ]; then
            echo "MISSING (imagenes_producto): $url"
        fi
    fi
done

# Check productos_variantes.imagen_url
psql -U $DB_USER -d $DB_NAME -h localhost -t -A -c "SELECT imagen_url FROM productos_variantes WHERE imagen_url LIKE '/static/uploads/%'" | while IFS= read -r url; do
    url=$(echo "$url" | tr -d '[:space:]')
    if [ -n "$url" ]; then
        file="/var/www/kharis-store$url"
        if [ ! -f "$file" ]; then
            echo "MISSING (variantes): $url"
        fi
    fi
done

echo "=== Check complete ==="
