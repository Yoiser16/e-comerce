-- Check localhost URLs
SELECT 'productos.imagen_principal' as campo, COUNT(*) as total FROM productos WHERE imagen_principal LIKE '%localhost%'
UNION ALL
SELECT 'productos_variantes.imagen_url', COUNT(*) FROM productos_variantes WHERE imagen_url LIKE '%localhost%'
UNION ALL
SELECT 'imagenes_producto.url', COUNT(*) FROM imagenes_producto WHERE url LIKE '%localhost%'
UNION ALL
SELECT 'categorias.imagen', COUNT(*) FROM categorias WHERE imagen LIKE '%localhost%';

-- Show examples
SELECT 'PRODUCT EXAMPLES' as info, imagen_principal FROM productos WHERE imagen_principal LIKE '%localhost%' LIMIT 5;

-- Fix: strip http://localhost:8000 from all image URLs
UPDATE productos SET imagen_principal = REPLACE(imagen_principal, 'http://localhost:8000', '') WHERE imagen_principal LIKE '%localhost:8000%';
UPDATE productos_variantes SET imagen_url = REPLACE(imagen_url, 'http://localhost:8000', '') WHERE imagen_url LIKE '%localhost:8000%';
UPDATE imagenes_producto SET url = REPLACE(url, 'http://localhost:8000', '') WHERE url LIKE '%localhost:8000%';
UPDATE categorias SET imagen = REPLACE(imagen, 'http://localhost:8000', '') WHERE imagen LIKE '%localhost:8000%';

-- Fix any remaining localhost with other ports
UPDATE productos SET imagen_principal = REPLACE(imagen_principal, 'http://localhost', '') WHERE imagen_principal LIKE '%localhost%';
UPDATE productos_variantes SET imagen_url = REPLACE(imagen_url, 'http://localhost', '') WHERE imagen_url LIKE '%localhost%';
UPDATE imagenes_producto SET url = REPLACE(url, 'http://localhost', '') WHERE url LIKE '%localhost%';
UPDATE categorias SET imagen = REPLACE(imagen, 'http://localhost', '') WHERE imagen LIKE '%localhost%';

-- Verify
SELECT 'AFTER FIX - productos' as campo, COUNT(*) FROM productos WHERE imagen_principal LIKE '%localhost%'
UNION ALL
SELECT 'AFTER FIX - variantes', COUNT(*) FROM productos_variantes WHERE imagen_url LIKE '%localhost%'
UNION ALL
SELECT 'AFTER FIX - imagenes', COUNT(*) FROM imagenes_producto WHERE url LIKE '%localhost%'
UNION ALL
SELECT 'AFTER FIX - categorias', COUNT(*) FROM categorias WHERE imagen LIKE '%localhost%';

-- Show fixed examples
SELECT 'FIXED EXAMPLES' as info, imagen_principal FROM productos WHERE imagen_principal IS NOT NULL LIMIT 5;
