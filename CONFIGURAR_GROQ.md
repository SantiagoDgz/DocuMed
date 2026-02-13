# IA Médica Educativa con Groq

## 📋 Descripción

Sistema de IA médica educativa que proporciona:
- ✓ Análisis de síntomas (NO diagnósticos)
- ✓ Información sobre interacciones de medicamentos
- ✓ Almacenamiento de historial médico
- ✓ Integración con Groq API para respuestas avanzadas

⚠️ **IMPORTANTE**: Esta IA es **educativa solamente**, NO reemplaza diagnósticos médicos profesionales.

---

## 🚀 Paso 1: Obtener API Key de Groq

1. Abre https://console.groq.com
2. Crea una cuenta o inicia sesión
3. Ve a **"API Keys"** en el menú izquierdo
4. Haz clic en **"Create New API Key"**
5. Copia la clave generada

---

## 🔧 Paso 2: Configurar en DocuMed

### Opción A: Configurar en el código (simple)

Abre `web_ia.py` y busca:

```python
GROQ_API_KEY = ""  # ← Pon aquí tu API key
```

Reemplaza con tu clave:

```python
GROQ_API_KEY = "gsk_tu_clave_aqui"
```

### Opción B: Usar variable de entorno (recomendado para producción)

**En Windows PowerShell:**
```powershell
$env:GROQ_API_KEY = "gsk_tu_clave_aqui"
```

**En el símbolo del sistema (CMD):**
```cmd
set GROQ_API_KEY=gsk_tu_clave_aqui
```

---

## 📚 Cómo Usar la IA Médica

### 1. Analizar Síntomas

```python
from medical_ai import IAMedicaEducativa

ia = IAMedicaEducativa()
analisis = ia.analizar_sintomas(['fiebre', 'tos'])
print(analisis)
```

### 2. Verificar Interacciones de Medicamentos

```python
interacciones = ia.verificar_interacciones(['warfarina', 'ibuprofeno'])
print(interacciones)
```

### 3. Guardar Historial

```python
ia.guardar_sintomas('paciente_123', ['dolor_cabeza'], 'Comenzó hace 2 días')
```

### 4. Obtener Historial

```python
historial = ia.obtener_historial('paciente_123')
print(historial)
```

---

## 🌐 API REST

### Analizar Síntomas

**POST** `/api/medical/sintomas`

```json
{
  "paciente_id": "pac123",
  "sintomas": ["fiebre", "tos"],
  "notas": "Síntomas desde hace 3 días"
}
```

### Verificar Medicamentos

**POST** `/api/medical/medicamentos`

```json
{
  "medicamentos": ["warfarina", "ibuprofeno"]
}
```

### Obtener Historial

**GET** `/api/medical/historial/<paciente_id>`

### Guardar Consulta

**POST** `/api/medical/guardar-consulta`

```json
{
  "paciente_id": "pac123",
  "tipo": "síntomas",
  "contenido": "Consulta sobre dolor de cabeza"
}
```

---

## 📁 Estructu de Archivos

- `medical_ai.py` - Clase principal IAMedicaEducativa
- `medical_ia_routes.py` - Rutas Flask para API
- `datos_medicos.json` - Base de datos (se crea automáticamente)
- `web_ia.py` - Configuración Flask y chat con Groq

---

## ⚠️ Responsabilidades y Limitaciones

✓ **Sí hace la IA:**
- Información educativa sobre síntomas
- Sugerencias sobre interacciones de drogas
- Almacenamiento de historiales

❌ **NO hace la IA:**
- Diagnosticar enfermedades
- Reemplazar atención médica profesional
- Proporcionar tratamientos específicos

**Siempre recomienda:** "Por favor, consulta con un profesional médico para evaluación completa"

---

## 🔗 Modelos Disponibles en Groq

- `mixtral-8x7b-32768` - Multiuso, rápido
- `llama2-70b-4096` - Lenguaje especializado
- `gemma-7b-it` - Ligero, respuestas cortas

---

## 📞 Soporte

Para problemas con Groq: https://console.groq.com/docs

---

**Última actualización:** Febrero 2026
