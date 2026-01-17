# Scripts de Utilidad - E-Commerce

Scripts para validacion, testing y operaciones del sistema.

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
