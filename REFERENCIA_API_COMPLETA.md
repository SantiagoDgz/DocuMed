# 📚 REFERENCIA COMPLETA DE FUNCIONES

## Sistema Médico Inteligente v2.0

---

## 🗂️ MÓDULO: pacientes_db.py

Gestor de base de datos de pacientes con almacenamiento JSON.

### Clase: GestorPacientes

#### `__init__(archivo_db='pacientes.json')`
Inicializa el gestor y carga datos.

#### `cargar_datos()`
Carga pacientes desde el archivo JSON.

#### `guardar_datos()`
Guarda pacientes en el archivo JSON (automático).

#### `agregar_paciente(datos_paciente) -> dict`
Registra un nuevo paciente.

**Parámetros:**
```python
{
    'nombre': str,
    'apellido': str,
    'cedula': str,
    'edad': int,
    'genero': str,  # 'M' o 'F'
    'telefono': str,
    'email': str,
    'direccion': str (opcional),
    'historia_medica': str (opcional),
    'alergias': str (opcional),
    'medicamentos': str (opcional),
    'peso': float (opcional),
    'altura': float (opcional),
    'presion_arterial': str (opcional),
}
```

**Retorna:**
```python
{
    'id': '00001',  # ID único generado
    'nombre': str,
    # ... todos los campos
    'diagnosticos': [],
    'tratamientos': [],
    'estudios': [],
    'timeline': [],
    'fecha_registro': str,
}
```

#### `obtener_paciente(id_paciente) -> dict`
Recupera un paciente por ID.

#### `actualizar_paciente(id_paciente, datos_actualizacion) -> bool`
Actualiza información del paciente.

#### `eliminar_paciente(id_paciente) -> bool`
Elimina un paciente.

#### `listar_pacientes() -> list`
Retorna lista de todos los pacientes.

#### `buscar_paciente(criterio, valor) -> list`
Busca pacientes por campo.

**Ejemplo:**
```python
db.buscar_paciente('nombre', 'Juan')
db.buscar_paciente('cedula', '1234567890')
```

#### `agregar_diagnostico(id_paciente, diagnostico, fecha=None)`
Agrega un diagnóstico al paciente.

#### `obtener_diagnosticos(id_paciente) -> list`
Retorna lista de diagnósticos.

**Retorna:**
```python
[
    {
        'diagnostico': 'Diabetes',
        'fecha': '2024-01-15'
    },
    # ...
]
```

#### `agregar_tratamiento(id_paciente, tratamiento, medicamento, dosis, duracion)`
Registra un tratamiento.

#### `obtener_tratamientos(id_paciente) -> list`
Retorna lista de tratamientos activos.

#### `agregar_estudio(id_paciente, tipo_estudio, resultado, fecha=None)`
Registra un examen/estudio.

#### `obtener_estudios(id_paciente) -> list`
Retorna lista de estudios realizados.

#### `agregar_evento_timeline(id_paciente, tipo_evento, descripcion)`
Agrega evento al timeline (automático en otras operaciones).

#### `obtener_timeline(id_paciente) -> list`
Retorna timeline cronológico ordenado.

---

## 🤖 MÓDULO: medical_ai.py

Motor de análisis inteligente para diagnóstico y recomendaciones.

### Clase: AnalisisAIMedico

#### `__init__()`
Inicializa el motor con conocimiento médico base.

**Atributos:**
- `diagnósticos_críticos` - Lista de diagnósticos graves
- `incompatibilidades_farmacologicas` - Medicinas incompatibles
- `edad_riesgos` - Riesgos por edad
- `rangos_vitales_normales` - Valores de referencia

#### `analizar_paciente(paciente) -> dict`
**Análisis completo del paciente.**

**Retorna:**
```python
{
    'alertas': [
        {
            'tipo': str,
            'nivel': 'bajo|medio|alto|critico',
            'mensaje': str,
            'acción': str
        },
        # ...
    ],
    'patrones': [
        {
            'nombre': str,
            'descripción': str,
            'implicación': str
        },
        # ...
    ],
    'recomendaciones': [str, ...],
    'score_riesgo': int,  # 0-100
    'resumen_clinico': str,
    'inconsistencias': [str, ...]
}
```

#### `_detectar_alertas(paciente) -> list`
Genera alertas inteligentes.

**Tipos de alertas:**
1. `diagnostico_critico` - Diagnósticos graves
2. `presion_anormal` - Presión arterial fuera de rango
3. `bmi_anormal` - IMC bajo o alto
4. `seguimiento_vencido` - Sin cita en mucho tiempo
5. `edad_riesgo` - Edad avanzada
6. `interaccion_medicamentos` - Medicina incompatible
7. `terapia_incompleta` - Diagnóstico sin tratamiento
8. `datos_incompletos` - Campos importantes vacíos

#### `_detectar_patrones(paciente) -> list`
Identifica síndromes y comorbilidades.

**Patrones detectados:**
- Síndrome metabólico
- Comorbilidades respiratorias
- Comorbilidades psiquiátricas
- Neuropatía diabética
- Fragilidad clínica
- Anomalías de frecuencia de consultas

#### `_generar_recomendaciones(paciente) -> list`
Sugiere acciones clínicas personalizadas.

**Basadas en:**
- Edad del paciente
- Diagnósticos presentes
- Estado de seguimiento
- IMC y vitales

#### `_calcular_riesgo(paciente) -> int`
Calcula score de riesgo 0-100.

**Factores considerados:**
- Edad (base)
- Diagnósticos (críticos +20, crónicos +10)
- Signos vitales (presión, FC anormal)
- BMI (bajo peso, sobrepeso, obesidad)
- Seguimiento (vencidos)

**Escala:**
- 0-25: Bajo riesgo
- 26-50: Riesgo moderado
- 51-75: Riesgo alto
- 76-100: Riesgo crítico

#### `resumir_historial(paciente) -> str`
Crea resumen ejecutivo del paciente.

#### `detectar_inconsistencias(paciente) -> list`
Valida completitud y consistencia de datos.

**Verifica:**
- Campos obligatorios
- Rangos válidos
- Consistencia temporal
- Coherencia clínica

---

## 🌐 MÓDULO: web_ia.py

Servidor Flask con API REST completa.

### Rutas principales

#### GET `/`
Interfaz de chat con IA (Claudia)

#### GET `/inicio`
Página de inicio con navegación

#### GET `/pacientes`
Interfaz de gestión de pacientes

#### GET `/medico-inteligente`
**Panel médico inteligente principal**

---

## 📡 API REST ENDPOINTS

### Gestión de Pacientes

#### `GET /api/pacientes`
Lista todos los pacientes.

**Respuesta:**
```json
{
    "exito": true,
    "pacientes": [
        {
            "id": "00001",
            "nombre": "Juan",
            // ...
        }
    ]
}
```

#### `POST /api/pacientes`
Registra nuevo paciente.

**Body:**
```json
{
    "nombre": "Juan",
    "apellido": "Pérez",
    // ... otros campos
}
```

#### `GET /api/pacientes/<id>`
Obtiene datos del paciente.

#### `PUT /api/pacientes/<id>`
Actualiza paciente.

#### `DELETE /api/pacientes/<id>`
Elimina paciente.

#### `GET /api/pacientes/buscar/<termino>`
Busca pacientes por nombre/cédula.

---

### Análisis de IA

#### `GET /api/analisis-paciente/<id>`
**Análisis completo con alertas, patrones, riesgo, recomendaciones.**

#### `GET /api/alertas-paciente/<id>`
Solo alertas inteligentes y score de riesgo.

#### `GET /api/recomendaciones/<id>`
Solo recomendaciones personalizadas.

#### `GET /api/resumen-clinico/<id>`
Resumen ejecutivo del paciente.

#### `GET /api/inconsistencias/<id>`
Detecta datos inconsistentes o incompletos.

---

### Información Clínica

#### `GET /api/pacientes/<id>/diagnosticos`
Lista diagnósticos.

#### `POST /api/pacientes/<id>/diagnosticos`
Agrega nuevo diagnóstico.

**Body:**
```json
{
    "diagnostico": "Diabetes Mellitus Tipo 2"
}
```

#### `GET /api/pacientes/<id>/tratamientos`
Lista tratamientos activos.

#### `POST /api/pacientes/<id>/tratamientos`
Agrega nuevo tratamiento.

**Body:**
```json
{
    "medicamento": "Metformina",
    "dosis": "500mg",
    "duracion": "3 meses"
}
```

#### `GET /api/pacientes/<id>/estudios`
Lista estudios realizados.

#### `POST /api/pacientes/<id>/estudios`
Registra nuevo estudio.

**Body:**
```json
{
    "tipo_estudio": "Laboratorio de sangre",
    "resultado": "Glucosa 150 mg/dL"
}
```

#### `GET /api/pacientes/<id>/timeline`
Timeline cronológico completo.

---

## 🎯 EJEMPLOS DE USO

### 1. Registrar Paciente

```python
from pacientes_db import GestorPacientes

db = GestorPacientes()
paciente = db.agregar_paciente({
    'nombre': 'Juan',
    'apellido': 'Pérez',
    'cedula': '1234567890',
    'edad': 58,
    'genero': 'M',
    'peso': 85,
    'altura': 175
})
print(f"Paciente creado: {paciente['id']}")
```

### 2. Analizar Paciente

```python
from medical_ai import AnalisisAIMedico

ia = AnalisisAIMedico()
paciente = db.obtener_paciente('00001')
analisis = ia.analizar_paciente(paciente)

print(f"Score de riesgo: {analisis['score_riesgo']}/100")
for alerta in analisis['alertas']:
    print(f"- {alerta['mensaje']}")
```

### 3. Agregar Diagnóstico

```python
db.agregar_diagnostico('00001', 'Diabetes Mellitus Tipo 2')
```

### 4. Ver Timeline

```python
timeline = db.obtener_timeline('00001')
for evento in timeline:
    print(f"{evento['fecha']} - {evento['descripcion']}")
```

### 5. Usar API (curl)

```bash
# Obtener paciente
curl http://localhost:5000/api/pacientes/00001

# Analizar con IA
curl http://localhost:5000/api/analisis-paciente/00001

# Agregar diagnóstico
curl -X POST http://localhost:5000/api/pacientes/00001/diagnosticos \
  -H "Content-Type: application/json" \
  -d '{"diagnostico":"Hipertension"}'
```

---

## 📊 ESTRUCTURA DE DATOS

### Paciente

```python
{
    'id': str,                  # '00001'
    'nombre': str,
    'apellido': str,
    'cedula': str,
    'edad': int,
    'genero': str,              # 'M' o 'F'
    'telefono': str,
    'email': str,
    'peso': float,
    'altura': float,
    'imc': float,
    'presion_arterial': str,    # '120/80'
    'alergias': str,
    'antecedentes': str,
    'diagnosticos': [           # Lista de diagnósticos
        {
            'diagnostico': str,
            'fecha': str        # 'YYYY-MM-DD'
        }
    ],
    'tratamientos': [           # Lista de tratamientos
        {
            'medicamento': str,
            'dosis': str,
            'duracion': str,
            'fecha_inicio': str
        }
    ],
    'estudios': [               # Lista de estudios
        {
            'tipo': str,
            'resultado': str,
            'fecha': str
        }
    ],
    'timeline': [               # Eventos cronológicos
        {
            'tipo': str,        # 'diagnostico', 'tratamiento', etc.
            'descripcion': str,
            'fecha': str
        }
    ],
    'fecha_registro': str,
    'ultima_actualizacion': str
}
```

### Alerta

```python
{
    'tipo': str,                # Tipo de alerta
    'nivel': str,               # 'bajo', 'medio', 'alto', 'critico'
    'mensaje': str,             # Descripción clara
    'acción': str               # Recomendación de acción
}
```

### Patrón

```python
{
    'nombre': str,
    'descripción': str,
    'implicación': str          # Implicancia clínica
}
```

---

## 🔧 CONFIGURACIÓN

El archivo `config_pacientes.py` (si existe) puede personalizar:

```python
PUERTO = 5000
DEBUG = True
ARCHIVO_BD = "pacientes.json"
REQUIERE_PASSWORD = False
CALCULAR_RIESGO = True
GENERAR_ALERTAS = True
```

---

## 🧪 TESTING

### Validar Sistema

```bash
python test_sistema_validacion.py
```

Verifica:
- ✓ Importación de módulos
- ✓ Base de datos funcional
- ✓ Motor de IA
- ✓ Archivos de interfaz
- ✓ Configuración de API
- ✓ Estructura de archivos

---

## 📚 DOCUMENTACIÓN RELACIONADA

- **GUIA_USUARIO_MEDICO.md** - Manual de usuario
- **CAPACIDADES_IA_DETALLADAS.md** - Detalles de IA
- **INSTALACION.md** - Instalación
- **README_v2_FINAL.md** - Resumen general

---

**Sistema Médico Inteligente v2.0**
*Referencia técnica completa*
