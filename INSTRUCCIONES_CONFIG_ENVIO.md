# 📦 Instrucciones: Configuración de Envíos (Backend + Panel Admin)

## ✅ Cambios Completados (Frontend)

1. ✅ Cambió el monto mínimo para envío gratis: **$500 → $300,000**
2. ✅ Cambió el costo de envío: **$15,000 → $30,000**
3. ✅ Eliminados emojis en mensajes de envío
4. ✅ Mejorada la validación: no muestra barra de progreso si ya alcanzó envío gratis
5. ✅ Corregido bug: toast y drawer del carrito ya no se superponen

---

## 🔧 Tareas Pendientes (Backend + Admin)

### 1️⃣ Crear Tabla en Base de Datos

Crear una nueva tabla `configuracion_envio` en PostgreSQL:

```sql
CREATE TABLE configuracion_envio (
    id SERIAL PRIMARY KEY,
    costo_envio_base INTEGER NOT NULL DEFAULT 30000,  -- Costo del envío en COP
    envio_gratis_desde INTEGER NOT NULL DEFAULT 300000,  -- Monto mínimo para envío gratis
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar configuración inicial
INSERT INTO configuracion_envio (costo_envio_base, envio_gratis_desde, activo)
VALUES (30000, 300000, true);
```

### 2️⃣ Crear Modelo en el Domain

**Archivo**: `src/domain/entities/configuracion_envio.py`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ConfiguracionEnvio:
    """Configuración de envíos del sistema"""
    id: Optional[int]
    costo_envio_base: int
    envio_gratis_desde: int
    activo: bool = True
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None
```

### 3️⃣ Crear Repositorio

**Archivo**: `src/infrastructure/persistence/configuracion_envio_repository.py`

```python
from typing import Optional
from src.domain.entities.configuracion_envio import ConfiguracionEnvio
from src.infrastructure.persistence.base_repository import BaseRepository

class ConfiguracionEnvioRepository(BaseRepository):
    
    async def obtener_activa(self) -> Optional[ConfiguracionEnvio]:
        """Obtiene la configuración de envío activa"""
        query = """
            SELECT id, costo_envio_base, envio_gratis_desde, activo,
                   fecha_creacion, fecha_modificacion
            FROM configuracion_envio
            WHERE activo = TRUE
            ORDER BY fecha_modificacion DESC
            LIMIT 1
        """
        row = await self.db.fetchrow(query)
        if not row:
            return None
        return ConfiguracionEnvio(**dict(row))
    
    async def actualizar(self, costo_envio: int, envio_gratis_desde: int) -> ConfiguracionEnvio:
        """Actualiza la configuración de envío"""
        query = """
            UPDATE configuracion_envio
            SET costo_envio_base = $1,
                envio_gratis_desde = $2,
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE activo = TRUE
            RETURNING id, costo_envio_base, envio_gratis_desde, activo,
                      fecha_creacion, fecha_modificacion
        """
        row = await self.db.fetchrow(query, costo_envio, envio_gratis_desde)
        return ConfiguracionEnvio(**dict(row))
```

### 4️⃣ Crear Endpoint en API

**Archivo**: `src/interfaces/api/configuracion_router.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from src.infrastructure.persistence.configuracion_envio_repository import ConfiguracionEnvioRepository
from src.infrastructure.auth.jwt_handler import require_role
from src.shared.enums.rol_enum import RolEnum

router = APIRouter(prefix="/configuracion", tags=["Configuración"])

class ConfiguracionEnvioResponse(BaseModel):
    costo_envio_base: int
    envio_gratis_desde: int

class ConfiguracionEnvioUpdate(BaseModel):
    costo_envio_base: int = Field(gt=0, description="Costo base del envío en COP")
    envio_gratis_desde: int = Field(gt=0, description="Monto mínimo para envío gratis")

@router.get("/envio", response_model=ConfiguracionEnvioResponse)
async def obtener_configuracion_envio(
    repo: ConfiguracionEnvioRepository = Depends()
):
    """Obtiene la configuración actual de envíos (público)"""
    config = await repo.obtener_activa()
    if not config:
        # Valores por defecto si no existe configuración
        return ConfiguracionEnvioResponse(
            costo_envio_base=30000,
            envio_gratis_desde=300000
        )
    return ConfiguracionEnvioResponse(
        costo_envio_base=config.costo_envio_base,
        envio_gratis_desde=config.envio_gratis_desde
    )

@router.put("/envio", response_model=ConfiguracionEnvioResponse)
async def actualizar_configuracion_envio(
    data: ConfiguracionEnvioUpdate,
    current_user = Depends(require_role(RolEnum.ADMIN)),
    repo: ConfiguracionEnvioRepository = Depends()
):
    """Actualiza la configuración de envíos (solo ADMIN)"""
    config = await repo.actualizar(data.costo_envio_base, data.envio_gratis_desde)
    return ConfiguracionEnvioResponse(
        costo_envio_base=config.costo_envio_base,
        envio_gratis_desde=config.envio_gratis_desde
    )
```

**Registrar en `main.py`:**

```python
from src.interfaces.api.configuracion_router import router as configuracion_router
app.include_router(configuracion_router)
```

### 5️⃣ Crear Vista en Panel Admin

**Archivo**: `frontend/src/components/admin/ConfiguracionEnvio.vue`

```vue
<template>
  <div class="p-6">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Configuración de Envíos</h2>
      <p class="text-sm text-gray-600 mt-1">Administra los costos de envío y el monto mínimo para envío gratis</p>
    </div>

    <!-- Formulario -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 max-w-2xl">
      <form @submit.prevent="guardarConfiguracion">
        
        <!-- Costo de Envío Base -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Costo de Envío Base (COP)
          </label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">$</span>
            <input 
              type="number" 
              v-model.number="config.costo_envio_base"
              required
              min="0"
              step="1000"
              class="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              placeholder="30000"
            />
          </div>
          <p class="text-xs text-gray-500 mt-1">Costo que se cobra cuando el pedido NO alcanza el monto mínimo</p>
        </div>

        <!-- Envío Gratis Desde -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Envío Gratis Desde (COP)
          </label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">$</span>
            <input 
              type="number" 
              v-model.number="config.envio_gratis_desde"
              required
              min="0"
              step="1000"
              class="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              placeholder="300000"
            />
          </div>
          <p class="text-xs text-gray-500 mt-1">Monto mínimo del carrito para aplicar envío gratis</p>
        </div>

        <!-- Vista Previa -->
        <div class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p class="text-sm text-blue-800 font-medium mb-2">Vista previa:</p>
          <ul class="text-sm text-blue-700 space-y-1">
            <li>• Compra de ${{ formatPrice(config.envio_gratis_desde - 10000) }}: Envío ${{ formatPrice(config.costo_envio_base) }}</li>
            <li>• Compra de ${{ formatPrice(config.envio_gratis_desde) }} o más: Envío GRATIS</li>
          </ul>
        </div>

        <!-- Botones -->
        <div class="flex gap-3">
          <button 
            type="submit"
            :disabled="guardando"
            class="px-6 py-3 bg-brand-600 text-white font-medium rounded-lg hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ guardando ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
          <button 
            type="button"
            @click="cargarConfiguracion"
            class="px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200"
          >
            Descartar
          </button>
        </div>
      </form>

      <!-- Mensaje de éxito -->
      <div v-if="mensaje" class="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-sm text-green-800">{{ mensaje }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiClient from '@/services/api'

export default {
  name: 'ConfiguracionEnvio',
  setup() {
    const config = ref({
      costo_envio_base: 30000,
      envio_gratis_desde: 300000
    })
    const guardando = ref(false)
    const mensaje = ref('')

    const formatPrice = (price) => {
      return new Intl.NumberFormat('es-CO').format(price)
    }

    const cargarConfiguracion = async () => {
      try {
        const response = await apiClient.get('/configuracion/envio')
        config.value = response.data
      } catch (error) {
        console.error('Error cargando configuración:', error)
      }
    }

    const guardarConfiguracion = async () => {
      guardando.value = true
      mensaje.value = ''
      try {
        await apiClient.put('/configuracion/envio', config.value)
        mensaje.value = 'Configuración actualizada correctamente'
        setTimeout(() => mensaje.value = '', 3000)
      } catch (error) {
        console.error('Error guardando configuración:', error)
        alert('Error al guardar la configuración')
      } finally {
        guardando.value = false
      }
    }

    onMounted(() => {
      cargarConfiguracion()
    })

    return {
      config,
      guardando,
      mensaje,
      formatPrice,
      cargarConfiguracion,
      guardarConfiguracion
    }
  }
}
</script>
```

**Agregar ruta en el router del admin:**

```javascript
{
  path: '/admin/configuracion-envio',
  name: 'ConfiguracionEnvio',
  component: () => import('@/components/admin/ConfiguracionEnvio.vue'),
  meta: { requiresAuth: true, requiresAdmin: true }
}
```

### 6️⃣ Actualizar Frontend para Consumir API

**Archivo**: `frontend/src/components/Home.vue` y `Checkout.vue`

Agregar en el `setup()`:

```javascript
const configEnvio = ref({
  costo_envio_base: 30000,
  envio_gratis_desde: 300000
})

// Cargar configuración al iniciar
onMounted(async () => {
  try {
    const response = await apiClient.get('/configuracion/envio')
    configEnvio.value = response.data
  } catch (error) {
    console.warn('Usando valores por defecto de envío')
  }
})

// Usar configEnvio.value.costo_envio_base en lugar de 30000
// Usar configEnvio.value.envio_gratis_desde en lugar de 300000
```

---

## 🎯 Resumen de Cambios

### Frontend (✅ Completado)
- Valores actualizados: $300k para envío gratis, $30k costo envío
- Sin emojis en mensajes
- Bug de superposición corregido
- Validación mejorada para envío gratis

### Backend (⏳ Pendiente)
- Tabla `configuracion_envio`
- Entity + Repository
- Endpoints GET/PUT `/configuracion/envio`
- Vista admin para configurar

---

## 📝 Notas Importantes

1. **Valores por defecto**: Si la API falla, el frontend usa $300k y $30k
2. **Seguridad**: Solo usuarios ADMIN pueden modificar la configuración
3. **Persistencia**: Los cambios se guardan en la base de datos
4. **Cache**: El frontend carga la configuración una vez al iniciar

---

**Fecha**: Enero 2026
**Estado**: Frontend completado, Backend pendiente
