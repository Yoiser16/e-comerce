# 📋 Instrucciones de Proyecto - Kharis Distribuidora E-commerce

> Este archivo es leído automáticamente por GitHub Copilot al inicio de cada conversación.
> Contiene las guías de diseño, arquitectura y buenas prácticas del proyecto.

---

## 🎨 GUÍA DE DISEÑO UI/UX

### Filosofía de Diseño
Este proyecto sigue un estilo **"Soft Luxury"** inspirado en marcas premium como Dior, Chanel y Fenty Beauty. El objetivo es transmitir elegancia, profesionalismo y confianza.

### Paleta de Colores
```
Primary (Brand):     #D81B60 (Magenta/Rosa - Solo CTAs principales)
Text Dark:           #1A1A1A
Text Medium:         #4A4A4A
Text Light:          #7A7A7A
Background:          #FAFAFA (Porcelana)
Nude/Blush:          #FAF5F2 a #F5EBE5
Gold Accent:         #C9A962 / #D4A85A
```

### Tipografía
- **Títulos**: `Playfair Display` (serif, clase `.font-luxury`)
- **Cuerpo**: `Inter` (sans-serif, system default)
- **Tamaños móvil**: Siempre usar clases responsivas (`text-sm sm:text-base lg:text-lg`)

### Principios de Diseño
1. **Mobile-First**: Todos los componentes deben verse bien en móvil primero
2. **Menos es Más**: Evitar elementos saturados, preferir espacios limpios
3. **Microinteracciones**: Transiciones suaves (`transition-all duration-300`)
4. **Glassmorphism sutil**: Header con `backdrop-blur` y transparencia
5. **CTAs compactos en móvil**: Botones más pequeños (`px-5 py-3 sm:px-7 sm:py-4`)

### Header / Navbar
- Estilo: Ultra-minimalista con glassmorphism
- Links: MAYÚSCULAS, `tracking-[0.12em]`, `font-size: 12px`
- Iconos: Stroke fino (`stroke-width="1.5"`)
- Clases: `.header-luxury`, `.header-luxury-scrolled`, `.nav-link-luxury`

### Botones
```html
<!-- CTA Principal - Negro elegante -->
<button class="bg-text-dark hover:bg-black text-white font-medium text-sm px-6 py-3 sm:px-8 sm:py-4 rounded-sm">

<!-- CTA Secundario - Borde fino -->
<button class="border border-text-dark/30 text-text-dark px-6 py-3 rounded-sm hover:border-text-dark">

<!-- CTA WhatsApp -->
<button class="bg-green-500 hover:bg-green-600 text-white px-5 py-3 sm:px-7 sm:py-3.5 rounded-full">
```

### Iconos
- Preferir iconos **stroke** (línea) sobre iconos filled
- Tamaño móvil: `w-4 h-4`, Desktop: `w-5 h-5`
- Color: `text-text-dark/70` o `text-[#8B7355]` para acentos

### Imágenes
- Videos locales: Usar `preload="auto"` para mejor calidad
- Altura mínima en móvil para videos: `min-h-[50vh]`
- Overlays: Gradientes suaves para legibilidad del texto

---

## 🏗️ ARQUITECTURA DEL PROYECTO

### Backend (Python/FastAPI)
```
src/
├── domain/          # Entidades, Value Objects, Eventos
├── application/     # Use Cases, DTOs, Commands, Queries
├── infrastructure/  # Persistencia, Auth, Messaging
├── interfaces/      # API REST, Permisos
└── shared/          # Utilidades, Constantes, Enums
```

### Frontend (Vue 3 + Vite)
```
frontend/src/
├── components/      # Componentes Vue
│   ├── Home.vue     # Landing principal
│   ├── Login.vue    # Autenticación
│   └── admin/       # Panel de administración
├── router/          # Vue Router
├── services/        # API calls (axios)
└── assets/          # Recursos estáticos
```

### Patrón de Diseño Backend
- **Domain-Driven Design (DDD)**
- **CQRS** (Commands/Queries separados)
- **Repository Pattern** para persistencia

---

## ⚠️ REGLAS IMPORTANTES

### NO HACER ❌
1. **NO generar archivos basura** (temporales, backups, etc.)
2. **NO crear archivos de test** que no se eliminen después de validar
3. **NO dejar `console.log` en producción**
4. **NO usar `!important` en CSS salvo casos extremos**
5. **NO crear componentes duplicados** - reutilizar existentes
6. **NO ignorar la vista móvil** - siempre revisar responsividad
7. **NO usar `backdrop-blur-sm` ni `backdrop-blur`** - afecta el rendimiento significativamente

### SÍ HACER ✅
1. **Eliminar tests temporales** inmediatamente después de validar
2. **Usar clases Tailwind responsivas** (`sm:`, `lg:`, etc.)
3. **Mantener consistencia** con el estilo de diseño luxury
4. **Documentar cambios importantes** en commits descriptivos
5. **Validar errores** después de cada edición (`get_errors`)
6. **Optimizar para móvil primero** - es la prioridad principal

### Tests y Validación
```bash
# Si necesitas crear un test temporal:
# 1. Créalo
# 2. Ejecútalo
# 3. ELIMÍNALO inmediatamente después

# Ejemplo:
python scripts/test_temporal.py && rm scripts/test_temporal.py
```

---

## 📱 BREAKPOINTS RESPONSIVOS

```css
/* Móvil (default) */
/* sm: 640px+ */
/* md: 768px+ */
/* lg: 1024px+ */
/* xl: 1280px+ */
```

### Tamaños Típicos
| Elemento | Móvil | Tablet (sm) | Desktop (lg) |
|----------|-------|-------------|--------------|
| Padding X | `px-4` | `px-6` | `px-12` |
| Botón | `px-5 py-3` | `px-6 py-3.5` | `px-8 py-4` |
| Texto CTA | `text-sm` | `text-sm` | `text-base` |
| Iconos | `w-4 h-4` | `w-5 h-5` | `w-6 h-6` |
| Floating Btns | `w-12 h-12` | `w-14 h-14` | `w-16 h-16` |

---

## 🔧 COMANDOS ÚTILES

```bash
# Frontend
cd frontend && npm run dev    # Desarrollo
cd frontend && npm run build  # Producción

# Backend
cd src && uvicorn main:app --reload  # Desarrollo

# Python environment
source venv/bin/activate
```

---

## 📝 COMMITS

Usar formato convencional:
```
feat: nueva funcionalidad
fix: corrección de bug
style: cambios de UI/CSS
refactor: restructuración de código
docs: documentación
chore: mantenimiento
```

---

## 🎯 PRIORIDADES DEL PROYECTO

1. **Experiencia Móvil** - 70% del tráfico viene de móviles
2. **Velocidad de carga** - Optimizar imágenes y assets
3. **Diseño Premium** - Mantener estética de lujo
4. **Usabilidad** - Flujos de compra simples e intuitivos

---

*Última actualización: Enero 2026*
