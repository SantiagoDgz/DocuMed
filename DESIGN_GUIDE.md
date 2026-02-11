# HVIRFILL - Guía de Diseño y Branding

## Paleta de Colores

### Colores Primarios
- **Primario Oscuro**: `#1a1a2e` - Azul oscuro profundo para fondos y títulos
- **Secundario**: `#16213e` - Azul más claro para elementos secundarios
- **Fondo Claro**: `#f8f9fa` - Gris muy claro para fondos generales

### Colores de Énfasis (Accent)
- **Accent Brillante**: `#00d4ff` - Cyan brillante (Logo - elemento primario)
- **Accent Luz**: `#64e4ff` - Cyan claro (variante)

### Colores de Texto
- **Texto Oscuro**: `#0f1621` - Negro suave para cuerpo de texto
- **Texto Claro**: `#8899aa` - Gris azulado para texto secundario

### Colores de Estado
- **Éxito**: `#00d084` - Verde para estados positivos
- **Error**: `#ff4757` - Rojo para alertas
- **Advertencia**: `#ffa500` - Naranja para avisos
- **Blanco**: `#ffffff` - Blanco puro

## Tipografía

### Fuentes
- **Titulares**: `Playfair Display` (serif) - Elegante, sofisticado
- **Cuerpo**: `Poppins` (sans-serif) - Moderna, legible

### Tamaños Recomendados
- **H1**: 48px (header principal)
- **H2**: 28-32px (secciones)
- **H3**: 22-24px (subsecciones)
- **Etiquetas**: 13px, uppercase, letter-spacing: 0.5px
- **Cuerpo**: 14px
- **Pequeño**: 12-13px

### Pesos de Fuente
- 300: Light (descripcciones, subtítulos)
- 400: Regular (cuerpo de texto)
- 500: Medium (énfasis moderado)
- 600: Semibold (etiquetas, énfasis)
- 700: Bold (títulos, botones)

## Sombras y Efectos

```css
--shadow-sm: 0 4px 15px rgba(0, 0, 0, 0.08);
--shadow-md: 0 8px 32px rgba(0, 0, 0, 0.12);
--shadow-lg: 0 16px 48px rgba(0, 0, 0, 0.16);
```

## Componentes Clave

### Botones
- **Botón Primario**: Gradient cyan (#00d4ff → #64e4ff), texto oscuro
- **Hover**: Elevar 2px, sombra aumentada
- **Padding**: 16px (altura mínima 48px para clickability)

### Formularios
- **Border**: 2px solid #f8f9fa
- **Focus**: Border #00d4ff, box-shadow con cyan sutil
- **Border-radius**: 12px
- **Transiciones**: all 0.3s ease

### Tarjetas
- **Background**: Blanco con border 1px rgba(0, 212, 255, 0.1)
- **Border-radius**: 16px
- **Padding**: 30-40px
- **Hover**: Aumentar sombra, cambiar border color

### Headers
- **Gradient**: 135deg, primario oscuro → secundario
- **Decoración**: Radial gradient sutil en cyan (top-right)
- **Color texto**: Cyan claro (#64e4ff)

## Espaciado

- Micro: 4px, 8px
- Pequeño: 12px, 16px
- Base: 20px, 24px
- General: 28px, 32px
- Grande: 40px, 50px
- Muy grande: 60px+

## Border Radius

- Inputs/buttons: 12px
- Tarjetas: 16px
- Headers/drawers: 20px+
- Badges/pills: 50px

## Animaciones

### Transiciones Estándar
```css
transition: all 0.3s ease;
```

### Efectos Especiales
- Slide in: 0.3s translateY(-10px)
- Hover elevation: translateY(-2px)
- Logo animation: gradient glow

## Páginas Rediseñadas

✅ **login.html** - Login elegante con gradient
✅ **home.html** - Dashboard principal con opciones
✅ **citas.html** - Sistema de citas completo
✅ **recetas.html** - Gestión de recetas digitales
✅ **laboratorios.html** - Sistema de laboratorios

## Componentes Standart CSS

Referencia: `docs/styles-global.css`

Contiene:
- Variables CSS (:root)
- Estilos base (*, html, body)
- Tipografía (h1, h2, a)
- Componentes reutilizables (.btn, .card, .alert)
- Utilidades (.text-center, .mt-20, etc)

## Cómo Usar

### En HTML Nuevo
```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">

<style>
    :root {
        --primary: #1a1a2e;
        --secondary: #16213e;
        --accent: #00d4ff;
        /* ... más variables */
    }
</style>
```

### Estructura de Página
```html
<div class="container">
    <div class="header">
        <div class="header-content">
            <h1>Título</h1>
            <p>Subtítulo</p>
        </div>
    </div>

    <div class="content">
        <div class="card">
            <!-- Contenido -->
        </div>
    </div>
</div>
```

## Mejores Prácticas

1. **Consistencia de color**: Usa solo los colores de la paleta
2. **Espaciado uniforme**: Mantén múltiplos de 4px o 8px
3. **Tipografía clara**: Playfair para títulos, Poppins para contenido
4. **Feedback visual**: Hover effects en todo elemento interactivo
5. **Responsividad**: Mobile-first, breakpoint en 768px
6. **Accesibilidad**: Contraste mínimo 4.5:1 en texto

## Sistema de Alertas

```html
<div class="alert alert-success show">
    ✓ Operación exitosa
</div>

<div class="alert alert-error show">
    ✗ Error en la operación
</div>
```

## Animaciones Transición

- **Fade in**: 0.3s ease (por defecto)
- **Slide (Y axis)**: translateY(-10px)
- **Hover scale**: translateY(-2px)
- **Smooth scroll**: scroll-behavior: smooth

---

**Última actualización**: Febrero 2026
**Versión**: 2.0 - Rediseño HVIRFILL
