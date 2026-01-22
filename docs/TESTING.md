# 🧪 Guía de Testing

## Ejecución de Pruebas

El proyecto utiliza `pytest` y scripts personalizados para validar diferentes capas del sistema.

### Tests Unitarios

Ejecutar todos los tests unitarios con PyTest:

```bash
pytest
```

### Tests de Integración y Scripts

Se disponen de scripts específicos en el directorio `scripts/` para validar flujos completos.

#### 1. Autenticación (`test_api_auth.py`)

Valida el ciclo de vida completo de la autenticación JWT y RBAC.

```bash
python scripts/test_api_auth.py
```

**Verificaciones:**
- Login exitoso (Admin, Operador, Lectura)
- Acceso denegado sin token (401)
- Permisos insuficientes (403)
- Refresh token válido
- Logout y blacklist de tokens

#### 2. Rate Limiting (`test_rate_limit.py`)

Verifica que las protecciones anti-abuso estén activas.

```bash
python scripts/test_rate_limit.py
```

**Escenarios:**
- Límite de intentos de login
- Límite de creación de órdenes rapidas

#### 3. Validación del Sistema (`validar_sistema.py`)

Health check general del backend.

```bash
python scripts/validar_sistema.py
```

## Reporte de QA

Para ver el historial de pruebas y correcciones, consultar:
- `docs/QA_REPORT_FINAL.md`
