# 🎨 Generador de Imágenes - Claudia AI

## ¿Qué se agregó?

Se ha añadido la capacidad de **generar imágenes usando IA** a tu aplicación Claudia AI. Ahora puedes crear imágenes con solo decirle a Claudia qué quieres.

---

## ⚡ Características Nuevas

### 1. **Generador de Imágenes Integrado**
- Genera imágenes directamente en el chat
- Usa el modelo **Stable Diffusion** (IA para generar imágenes)
- Las imágenes se muestran en la conversación

### 2. **Dos formas de generar imágenes:**

#### **Opción 1: Botón de Generar Imagen**
- Click en el botón `🎨 Generar Imagen` en la barra de controles
- Escribe una descripción detallada
- La IA genera y muestra la imagen

#### **Opción 2: Escribir en el chat**
- Escribe directamente: "Genera una imagen de..."
- Palabras clave que funcionan:
  - "genera imagen"
  - "crea una imagen"
  - "dibuja"
  - "pinta"
  - "imagen de"
  - "crear imagen"
  - "generar imagen"

---

## 📝 Ejemplos de Uso

### Ejemplo 1 - Botón
```
1. Click en "🎨 Generar Imagen"
2. Escribe: "Un gato naranja jugando con una pelota en el parque"
3. ¡La IA genera la imagen!
```

### Ejemplo 2 - Chat
```
Tú: "Genera una imagen de un castillo medieval al atardecer"
Claudia: ✨ Genera la imagen
```

### Ejemplo 3 - Especificidad
```
"Crea una imagen de un astronauta en la luna, 
estilo pixel art retro, colores vivos y neón"
```

---

## 🎯 Consejos para Mejores Resultados

1. **Sé específico**: Incluye detalles sobre:
   - Colores
   - Estilo artístico (cartoon, realista, pixel art, etc.)
   - Ambiente o escena
   - Objetos principales

2. **Ejemplo de buena descripción:**
   ```
   "Un dragón dorado volando sobre montañas nevadas, 
   estilo fantasy épico, luces mágicas azules"
   ```

3. **Evita descripciones vagas:**
   ```
   ❌ "Una imagen bonita"
   ✅ "Una puesta de sol en la playa con palmeras y colores naranjas y rosados"
   ```

---

## 🔧 Cambios Técnicos Realizados

### Backend (web_ia_simple.py)
- ✅ Importadas librerías: `Pillow`, `requests`, `base64`
- ✅ Agregado método `generar_imagen()` en la clase `IAClaudia`
- ✅ Nueva ruta `/generar-imagen` para generar imágenes
- ✅ Detecta palabras clave de imagen en el chat
- ✅ Retorna imágenes en formato base64

### Frontend (index.html)
- ✅ Agregados estilos para mostrar imágenes
- ✅ Nueva función `agregarMensajeConImagen()`
- ✅ Botón `🎨 Generar Imagen` en la barra de controles
- ✅ Función `abrirGeneradorImagenes()` con cuadro de diálogo
- ✅ Función `generarImagenDirecta()` para llamar al servidor
- ✅ Manejo de imágenes en base64

---

## ⚙️ Dependencias Instaladas

```
Pillow     - Procesamiento de imágenes
requests   - Peticiones HTTP a la API
```

Instáladas con:
```bash
pip install Pillow requests
```

---

## 🌐 API de Generación de Imágenes

Se está usando **Hugging Face Inference API** con modelos:
1. **Stable Diffusion 3** (modelo principal)
2. **Stable Diffusion v1.5** (modelo alternativo si el primero no está disponible)

⚠️ **Nota**: El token de API (`hf_api_key`) en el código es de demostración. Para usar en producción, reemplázalo con tu propio token de [Hugging Face](https://huggingface.co)

---

## 📱 Uso en el Chat

### Estructura de la conversación:

```
Usuario: "Genera una imagen de un gato"
         ↓
Claudia: (detecta palabras clave "genera imagen")
         ↓
         (llama al endpoint /generar-imagen)
         ↓
         ✨ Muestra la imagen en el chat
         + Texto descriptivo de la generación
```

---

## ⏱️ Tiempo de Generación

- **Primera llamada**: 10-30 segundos (carga del modelo)
- **Llamadas siguientes**: 5-15 segundos (más rápido en caché)

---

## ✨ Nuevas Rutas API

### POST /generar-imagen
```json
Solicitud:
{
  "descripcion": "Un gato naranja en la playa"
}

Respuesta:
{
  "success": true,
  "mensaje": "✨ Imagen generada exitosamente",
  "imagen_base64": "iVBORw0KGgoAAAANSUhEUgAAAA...",
  "timestamp": "14:30:45"
}
```

---

## 🎨 Ejemplos Inspiradores

Prueba con estas descripciones:

1. **Fantasía**: "Un mago lanzando hechizos mágicos, fuegos artificiales de colores, estilo anime"

2. **Naturaleza**: "Un bosque encantado con luces mágicas, hongos brillantes, estilo Studio Ghibli"

3. **Futurismo**: "Cyborg femenino en una ciudad futurista neon, lluvia, cyberpunk"

4. **Artístico**: "Retrato abstracto con colores vibrantes y formas geométricas"

5. **Surrealismo**: "Escalera flotante en el espacio llevando a una galaxia"

---

## 🐛 Solución de Problemas

### La imagen tarda mucho
- Es normal en la primera llamada (carga del modelo)
- Espera 20-30 segundos

### Error "No se pudo generar la imagen"
- El token de API no es válido
- Obtén tu token en [Hugging Face](https://huggingface.co/settings/tokens)
- Reemplázalo en `web_ia_simple.py` línea ~16

### Imagen no se ve
- Verifica la consola del navegador (F12)
- Asegúrate que el servidor está corriendo correctamente

---

## 🚀 Próximas Mejoras Posibles

- [ ] Guardar imágenes generadas
- [ ] Galería de imágenes históricas
- [ ] Edición de imágenes generadas
- [ ] Diferentes modelos de IA (DALL-E, Midjourney)
- [ ] Opciones de tamaño y calidad

---

## 📞 Soporte

Si tienes problemas:
1. Revisa la consola del navegador (F12 → Console)
2. Verifica los logs del servidor Flask
3. Asegúrate de tener las dependencias instaladas

---

¡Diviértete generando imágenes! 🎨✨
