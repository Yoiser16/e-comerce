# 🔐 Seguridad y Autenticación

## Sistema de Autenticación JWT

El sistema implementa un mecanismo robusto de tokens JWT:

- **Access Token**: Validez corta (15 min). Se envía en header `Authorization: Bearer <token>`.
- **Refresh Token**: Validez larga (1 día). Rotativo (cambia con cada uso).
- **Blacklist**: Invalidation de tokens al hacer logout.

## Roles y Permisos (RBAC)

| Rol | Acceso | Descripción |
|-----|--------|-------------|
| **ADMIN** | Total | Control completo del sistema, incluyendo usuarios y eliminación de recursos. |
| **OPERADOR** | Lectura/Escritura | Gestión diaria: crear/editar productos, clientes y órdenes. No puede eliminar. |
| **LECTURA** | Solo Lectura | Acceso de consulta a reportes y listas. |

## Protección Anti-Abuso (Rate Limiting)

Implementado a nivel de aplicación para prevenir ataques de fuerza bruta y DDoS:

| Tipo | Límite | Descripción |
|------|--------|-------------|
| Anónimo | 50/min | Usuarios no autenticados |
| Autenticado | 200/min | Usuarios con token válido |
| Login | 5/min | Prevención fuerza bruta en `/auth/login` |
| Órdenes | 20/min | Prevención fraude en creación de órdenes |

## Auditoría

Todos los accesos a la API son auditados automáticamente y almacenados en la base de datos para cumplimiento y trazabilidad.

```python
# Ejemplo de modelo de auditoría
class AuditoriaAccesoAPI(models.Model):
    usuario = models.ForeignKey(...)
    endpoint = models.CharField(...)
    metodo = models.CharField(...)
    ip_origen = models.GenericIPAddressField(...)
    resultado_exitoso = models.BooleanField(...)
```
