# Scripts de Utilidad - E-Commerce

Scripts para validacion, testing y operaciones del sistema.

---

## 🆕 NUEVO: crear_orden_test.sh

**Script bash para generar órdenes de prueba rápidamente.**

### Uso:
```bash
# Desde la raíz del proyecto
bash scripts/crear_orden_test.sh

# O darle permisos de ejecución
chmod +x scripts/crear_orden_test.sh
./scripts/crear_orden_test.sh
```

### Características:
- ✅ Genera datos aleatorios realistas (nombres, direcciones, teléfonos)
- ✅ Crea entre 1 y 3 productos por orden
- ✅ Calcula subtotales y envío automáticamente
- ✅ Muestra información detallada de la orden creada
- ✅ Perfecto para probar el sistema de notificaciones en tiempo real del panel admin

### Requisitos:
- Servidor backend corriendo en `http://localhost:8000`
- `curl` instalado en el sistema

### Probar Notificaciones en Tiempo Real:

1. **Inicia el servidor backend:**
   ```bash
   cd src && uvicorn main:app --reload
   ```

2. **Inicia el frontend:**
   ```bash
   cd frontend && npm run dev
   ```

3. **Abre el panel de administración** → Sección "Órdenes"
   - El sistema ahora actualiza automáticamente cada 5 segundos

4. **Ejecuta el script:**
   ```bash
   bash scripts/crear_orden_test.sh
   ```

5. **Observa las mejoras:**
   - 🔔 Suena una notificación sonora
   - 🔵 La nueva orden aparece con indicador azul (no vista)
   - 📱 Aparece notificación del navegador (si está permitido)
   - 🔄 Panel se actualiza sin refrescar

---

## Scripts Disponibles

### validar_sistema.py

Validacion end-to-end del sistema completo.

**Uso:**
```bash
python scripts/validar_sistema.py
```

**Funcionalidad:**
- Valida conexion PostgreSQL
- Prueba creacion de clientes
- Verifica reglas de negocio
- Valida persistencia y recuperacion
- Muestra estadisticas

---

### shell_commands.py

Comandos pre-configurados para Django shell.

**Uso:**
```bash
python manage.py shell
exec(open('scripts/shell_commands.py').read())
```

---

## Comandos Django Management (Recomendados)

```bash
# Validar sistema
python manage.py validar_sistema

# Verificar base de datos
python manage.py check_database

# Shell interactivo
python manage.py shell
```

---

**[← README Principal](../README.md)**
