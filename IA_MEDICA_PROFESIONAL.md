# 🏥 IA Médica Profesional - Herramienta Clínica

**Estado:** ✅ Operacional | **Versión:** 2.0 Profesional | **Tipo:** Sistema de Soporte Clínico

---

## 📋 Descripción General

IA Médica Profesional es una **herramienta de soporte clínico** diseñada para **ayudar a médicos** en:

✅ **Búsqueda y gestión de pacientes**  
✅ **Análisis automático de resultados de laboratorio**  
✅ **Generación inteligente de alertas**  
✅ **Identificación de tendencias clínicas**  
✅ **Consultas médicas con Groq AI**  
✅ **Historial y seguimiento de pacientes**  

---

## 🔧 Funcionalidades Principales

### 1. 🔍 Búsqueda de Pacientes

Busca pacientes por múltiples criterios:

```python
# Buscar por nombre
resultado = ia.buscar_paciente('nombre', 'Juan')

# Buscar por cédula
resultado = ia.buscar_paciente('cedula', '12345678')

# Buscar por ID
resultado = ia.buscar_paciente('id', 'pac001')
```

**API REST:**
```
POST /api/medical/buscar-paciente
Body: {"criterio": "nombre", "valor": "Juan"}
```

---

### 2. 🧪 Análisis de Laboratorio

Lee y analiza automáticamente resultados de lab:

```python
resultados = {
    'glucosa': 280,
    'hemoglobina': 9.2,
    'creatinina': 1.8,
    'presion_sistolica': 165
}

análisis = ia.analizar_resultados_laboratorio('pac001', resultados)
```

**Detecta automáticamente:**
- ✓ Valores fuera de rango
- ✓ Resultados críticos
- ✓ Patrones peligrosos
- ✓ Genera alertas automáticas

---

### 3. ⚠️ Sistema de Alertas

Alertas inteligentes con 4 niveles:

| Nivel | Símbolo | Acción |
|-------|---------|--------|
| CRÍTICO | 🔴 | Intervención inmediata |
| ALTO | 🟠 | Revisión urgente |
| MODERADO | 🟡 | Monitoreo |
| NORMAL | 🟢 | Monitoreo rutinario |

```python
# Obtener alertas
alertas = ia.obtener_alertas_paciente('pac001', solo_activas=True)

# Generar alerta manual
alerta = ia.generar_alerta_manual(
    'pac001',
    'alergia_medicamento',
    'Paciente alérgico a penicilina',
    'CRÍTICO'
)
```

---

### 4. 👤 Perfil de Paciente

Visión completa del paciente:

```python
perfil = ia.obtener_perfil_paciente('pac001')
```

Incluye:
- Información personal
- Antecedentes médicos
- Medicamentos actuales
- Alergias y restricciones
- Alertas activas
- Último análisis
- Última visita

---

### 5. 📈 Comparación de Tendencias

Analiza cambios en el tiempo:

```python
tendencias = ia.comparar_análisis_temporal('pac001', últimos_n=5)
```

Muestra:
- Evolución de pruebas de laboratorio
- Patrones en el tiempo
- Cambios significativos

---

### 6. 💬 Consulta con Groq AI

Accede a inteligencia artificial médica:

```python
chat = IAMedicaChat()
respuesta = chat.consultar_médico(
    "¿Qué hacer ante glucosa de 280?",
    "Paciente diabético tipo 2, edad 65"
)
```

**API REST:**
```
POST /api/medical/consultar-groq
Body: {
    "consulta": "¿Qué hacer?",
    "contexto": "Paciente diabético..."
}
```

---

## 📊 Rangos de Laboratorio Integrados

La IA conoce automáticamente 20+ pruebas comunes:

| Prueba | Rango Normal | Unidad |
|--------|--------------|--------|
| Glucosa | 70-100 | mg/dL |
| Hemoglobina | 12-17.5 | g/dL |
| Creatinina | 0.7-1.3 | mg/dL |
| Presión Sistólica | 90-120 | mmHg |
| Colesterol Total | 0-200 | mg/dL |
| Potasio | 3.5-5 | mEq/L |
| ... y más |

---

## 🚀 API REST Completa

### Buscar Paciente
```
POST /api/medical/buscar-paciente
{
    "criterio": "nombre",
    "valor": "Juan"
}
```

### Obtener Perfil
```
GET /api/medical/perfil-paciente/<paciente_id>
```

### Analizar Laboratorio
```
POST /api/medical/analizar-laboratorio
{
    "paciente_id": "pac001",
    "resultados": {
        "glucosa": 280,
        "hemoglobina": 9.5
    }
}
```

### Obtener Alertas
```
GET /api/medical/alertas/<paciente_id>?solo_activas=true
```

### Generar Alerta
```
POST /api/medical/generar-alerta
{
    "paciente_id": "pac001",
    "tipo": "medicamento",
    "descripción": "...",
    "severidad": "CRÍTICO"
}
```

### Registrar Consulta
```
POST /api/medical/registrar-consulta
{
    "paciente_id": "pac001",
    "notas_médico": "...",
    "diagnóstico": "...",
    "recomendaciones": "..."
}
```

### Resumen Clínico
```
GET /api/medical/resumen-clínico/<paciente_id>
```

### Comparar Análisis
```
GET /api/medical/comparar-análisis/<paciente_id>?últimos=5
```

### Consultar Groq
```
POST /api/medical/consultar-groq
{
    "consulta": "¿Qué hacer?",
    "contexto": "Historia clínica..."
}
```

---

## 📁 Estructura de Datos

### Paciente
```json
{
    "id": "pac001",
    "nombre": "Juan",
    "apellido": "García",
    "cedula": "12345678",
    "edad": 65,
    "genero": "M",
    "email": "juan@example.com",
    "diagnósticos": ["Hipertensión", "Diabetes"],
    "medicamentos": ["Losartán 50mg"],
    "alergias": "Penicilina",
    "última_consulta": "2026-02-01"
}
```

### Análisis
```json
{
    "paciente_id": "pac001",
    "fecha": "2026-02-12T11:11:27",
    "resultados_analizados": [...],
    "anomalías": [...],
    "alertas_generadas": [...]
}
```

### Alerta
```json
{
    "paciente_id": "pac001",
    "fecha": "2026-02-12T11:11:27",
    "tipo": "resultado_crítico",
    "prueba": "Glucosa en ayunas",
    "valor": 280,
    "severidad": "CRÍTICO",
    "estado": "activa"
}
```

---

## 💾 Bases de Datos

- **datos_medicos.json** - Consultas, análisis, alertas
- **pacientes_db.json** - Información de pacientes

---

## ⚖️ Responsabilidades Clínicas

| ✅ AIA Hace | ❌ AIA NO Hace |
|-------------|---------------|
| Busca información rápido | Reemplaza diagnóstico médico |
| Detecta anomalías de laboratorio | Prescribe tratamientos |
| Genera alertas inteligentes | Toma decisiones finales |
| Propone análisis | Modifica histórico sin médico |
| Compara tendencias | Actúa sin supervisión |

**IMPORTANTE:** El médico siempre es responsable de las decisiones clínicas.

---

## 🎯 Casos de Uso

1. **Revisión Rápida de Paciente**
   - Buscar paciente
   - Ver perfil completo
   - Revisar alertas

2. **Ingreso de Resultados de Lab**
   - Cargar resultados
   - Sistema detecta anomalías
   - Genera alertas automáticamente

3. **Seguimiento de Tendencias**
   - Comparar últimos análisis
   - Identificar cambios
   - Ajustar tratamiento

4. **Consulta Médica Rápida**
   - Usar Groq para información
   - Revisar con especialistas
   - Tomar decisiones informadas

---

## ⚡ Ejemplo Completo

```python
from medical_ai import IAMedicaProfesional

ia = IAMedicaProfesional()

# 1. Buscar paciente
resultado = ia.buscar_paciente('cedula', '12345678')
paciente_id = resultado['resultados'][0]['id']

# 2. Obtener perfil
perfil = ia.obtener_perfil_paciente(paciente_id)
print(perfil)

# 3. Analizar nuevos resultados
análisis = ia.analizar_resultados_laboratorio(paciente_id, {
    'glucosa': 250,
    'hemoglobina': 8.5
})

# 4. Ver alertas generadas
alertas = ia.obtener_alertas_paciente(paciente_id, solo_activas=True)

# 5. Registrar consulta
consulta = ia.registrar_consulta(
    paciente_id,
    'Paciente con glucosa elevada',
    'Diabetes descontrolada',
    'Aumentar metformina'
)
```

---

## 🔐 Seguridad

- ✓ Datos en BD local (JSON)
- ✓ No se comparte información sin autorización
- ✓ Alertas inmediatas para situaciones críticas
- ✓ Auditoría de consultas médicas

---

## 📞 Soporte Groq

- Documentación: https://console.groq.com/docs
- API Key: https://console.groq.com
- Modelos disponibles: Mixtral, Llama2, Gemma

---

## 🎓 Próximas Versiones

- [ ] Dashboard web completo
- [ ] Importar DICOM de radiología
- [ ] ML para predicción de riesgos
- [ ] Integración con HIS
- [ ] Reportes automatizados

---

**Última actualización:** Febrero 2026  
**Responsable:** Médico licenciado  
**Nivel de Evidencia:** Soporte clínico  
**Cumplimiento:** Normativa médica local
