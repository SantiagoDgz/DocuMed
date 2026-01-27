# 🏥 Sistema Médico Inteligente - Guía Completa

## 📋 Descripción General

Sistema integral de gestión médica con inteligencia artificial, seguridad avanzada y sincronización en la nube. Una solución completa para clínicas y consultorios médicos modernos.

---

## ✨ Características Principales

### 1. **Gestión de Pacientes** 👥
- Registro completo de pacientes
- Datos demográficos y de contacto
- Historial médico integrado
- Búsqueda avanzada por nombre, apellido, cédula o ID
- Edición y actualización de datos

**Acceso:** `/pacientes`

---

### 2. **Captura de Datos Clínicos** 📋
Sistema completo para registrar información médica:

- **Signos Vitales**: Presión arterial, temperatura, frecuencia cardíaca, respiratoria, SpO2
- **Síntomas**: Registro detallado de síntomas del paciente
- **Diagnósticos**: Diagnósticos médicos profesionales
- **Tratamientos**: Planes de tratamiento y medicamentos
- **Estudios**: Resultados de pruebas y análisis
- **Notas Médicas**: Observaciones y recomendaciones

**Acceso:** `/captura-datos`

---

### 3. **Análisis y Reportes** 📊
Visualización avanzada de datos clínicos:

- Gráficos de evolución en tiempo real con Chart.js
- 6 tipos de gráficos: Presión, Temperatura, FC, FR, SpO2, Glucosa
- Tablas históricas detalladas
- Estadísticas por paciente
- **Exportación a PDF** con html2pdf.js
- Filtrado por rango de fechas

**Acceso:** `/analisis-reportes`

---

### 4. **Panel Médico Inteligente** 🤖
Sistema de IA para análisis clínico:

- Análisis automático de datos médicos
- Detección de alertas y anomalías
- Recomendaciones médicas inteligentes
- Chat conversacional con asistente IA
- Base de conocimientos médicos integrada

**Acceso:** `/medico-inteligente`

---

### 5. **Gestión de Citas Médicas** 📅
Sistema completo de agendamiento:

- Calendario interactivo
- Selección de fechas y horas disponibles
- Especialidades médicas
- Estados de cita (Programada, Confirmada, Cancelada)
- Recordatorios automáticos
- Información del motivo de consulta

**Acceso:** `/citas`

**Características:**
- Calendario navegable mes a mes
- 8 franjas horarias disponibles
- 5 especialidades médicas
- Confirmación de citas
- Historial de citas

---

### 6. **Sistema de Laboratorios** 🧪
Gestión completa de órdenes de laboratorio:

- Creación de órdenes de laboratorio
- 9 tipos de análisis disponibles
- Selección de laboratorio
- Prioridad de análisis (Rutina/Urgente)
- Carga de resultados
- Parámetros con rangos normales
- Estados: Pendiente → Completada

**Acceso:** `/laboratorios`

**Análisis Disponibles:**
- Hemograma Completo
- Panel Químico
- Perfil Lipídico
- Función Renal
- Función Hepática
- Función Tiroidea
- Prueba de Diabetes
- Prueba VIH

---

### 7. **Recetas Digitales** 💊
Sistema de prescripciones modernas:

- Creación de recetas digitales
- Información de medicamentos y dosis
- Fechas de vigencia
- Filtrado por estado (Vigentes, Vencidas)
- **Impresión directa**
- **Descarga en PDF**
- Identificación única de recetas

**Acceso:** `/recetas`

---

### 8. **Encriptación de Datos** 🔐
Protección avanzada de información sensible:

**Módulo: `encryption.py`**

#### Características:
- Cifrado AES-128 con Fernet
- Encriptación de datos sensibles:
  - Emails de pacientes
  - Números de teléfono
  - Cédulas de identidad
  - Direcciones
  - Datos médicos clasificados

#### API:
```python
from encryption import encriptador

# Encriptar datos
resultado = encriptador.cifrar_datos("dato sensible", "tipo")
hash_dato = resultado['hash']

# Desencriptar datos
dato_original = encriptador.descifrar_datos(hash_dato)

# Encriptar paciente completo
datos_cifrados = encriptador.cifrar_paciente(id_paciente, datos)

# Auditoría de acceso
encriptador.registrar_acceso_dato(hash, usuario, "lectura")
```

#### Endpoints REST:
- `POST /api/encriptar` - Encripta datos
- `GET /api/desencriptar/<hash>` - Desencripta datos (requiere autenticación)

---

### 9. **Sincronización en la Nube** ☁️
Backup automático y sincronización:

**Módulo: `cloud_sync.py`**

#### Características:
- Backups completos e incrementales
- Sincronización con múltiples servicios:
  - Almacenamiento local
  - Dropbox
  - Google Drive
  - AWS S3

#### Tipos de Backup:
- **Completo**: Copia todos los datos
- **Incremental**: Solo cambios desde último backup

#### API:
```python
from cloud_sync import sincronizador_nube

# Crear backup completo
backup = sincronizador_nube.crear_backup_completo(['pacientes.json'])

# Sincronizar con nube
resultado = sincronizador_nube.sincronizar_nube('local', archivos)

# Restaurar backup
sincronizador_nube.restaurar_backup('backup_20240101_120000')

# Estadísticas
stats = sincronizador_nube.obtener_estadisticas_backups()

# Limpiar backups antiguos
sincronizador_nube.limpiar_backups_antiguos(dias=30)
```

#### Endpoints REST:
- `POST /api/backup/crear` - Crea nuevo backup
- `GET /api/backup/listar` - Lista todos los backups
- `POST /api/backup/restaurar/<nombre>` - Restaura un backup
- `POST /api/sincronizar` - Sincroniza con servicio en la nube

**Acceso:** `/seguridad`

---

## 🔑 Usuarios Demo

Para probar el sistema, usa estas credenciales:

### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Rol:** Administrador del sistema

### Doctor
- **Usuario:** `doctor`
- **Contraseña:** `doctor123`
- **Rol:** Médico tratante

---

## 🚀 Instalación y Uso

### 1. **Iniciar el servidor**
```bash
python web_ia.py
```

El servidor se ejecutará en `http://localhost:5000`

### 2. **Acceder a las páginas**

| Sección | URL | Descripción |
|---------|-----|-------------|
| Inicio | `/` | Dashboard principal |
| Pacientes | `/pacientes` | Gestión de pacientes |
| Captura Datos | `/captura-datos` | Registro de datos clínicos |
| Análisis | `/analisis-reportes` | Gráficos y reportes |
| Panel IA | `/medico-inteligente` | Inteligencia artificial |
| Citas | `/citas` | Agendamiento de citas |
| Laboratorios | `/laboratorios` | Gestión de labs |
| Recetas | `/recetas` | Prescripciones digitales |
| Seguridad | `/seguridad` | Encriptación y backups |

---

## 📁 Estructura de Archivos

```
Sistema Médico/
├── web_ia.py                 # Servidor Flask principal
├── pacientes_db.py          # Gestor de base de datos JSON
├── medical_ai.py            # Motor de IA médica
├── encryption.py            # Módulo de encriptación
├── cloud_sync.py            # Módulo de sincronización
├── pacientes.json           # Base de datos de pacientes
├── datos_encriptados.json   # Registro de datos cifrados
├── templates/
│   ├── dashboard.html       # Página de inicio
│   ├── pacientes.html       # Gestión de pacientes
│   ├── captura_datos.html   # Formulario de datos clínicos
│   ├── analisis_reportes.html # Gráficos y reportes
│   ├── medico_inteligente.html # Panel de IA
│   ├── citas.html           # Sistema de citas
│   ├── laboratorios.html    # Gestión de laboratorios
│   ├── recetas.html         # Recetas digitales
│   ├── seguridad.html       # Encriptación y backup
│   ├── login.html           # Página de login
│   └── ...
└── __pycache__/             # Caché de Python
```

---

## 🔌 API REST Endpoints

### Pacientes
- `GET /api/pacientes` - Listar todos
- `POST /api/pacientes` - Crear nuevo
- `GET /api/pacientes/<id>` - Obtener uno
- `PUT /api/pacientes/<id>` - Actualizar
- `DELETE /api/pacientes/<id>` - Eliminar

### Datos Clínicos
- `POST /api/pacientes/<id>/sintomas` - Agregar síntomas
- `POST /api/pacientes/<id>/diagnostico` - Agregar diagnóstico
- `POST /api/pacientes/<id>/tratamiento` - Agregar tratamiento
- `POST /api/pacientes/<id>/estudio` - Agregar estudio
- `POST /api/pacientes/<id>/notas` - Agregar notas

### Encriptación
- `POST /api/encriptar` - Encriptar datos
- `GET /api/desencriptar/<hash>` - Desencriptar datos

### Backup y Cloud
- `POST /api/backup/crear` - Crear backup
- `GET /api/backup/listar` - Listar backups
- `POST /api/backup/restaurar/<nombre>` - Restaurar backup
- `POST /api/sincronizar` - Sincronizar con nube

### Citas
- `GET /api/citas` - Listar citas
- `POST /api/citas` - Crear cita

### Laboratorios
- `GET /api/laboratorios` - Listar órdenes
- `POST /api/laboratorios` - Crear orden

---

## 🔒 Seguridad

### Características Implementadas:
1. **Encriptación AES-128** para datos sensibles
2. **Hashing SHA-256** para contraseñas
3. **Tokens aleatorios** con secrets module
4. **Auditoría de acceso** a datos cifrados
5. **Backups encriptados** en múltiples servicios
6. **Permisos por usuario** configurable

### Mejores Prácticas:
- Siempre usa HTTPS en producción
- Cambia las contraseñas demo
- Realiza backups regularmente
- Configura encriptación de datos sensibles
- Mantén logs de auditoría

---

## 📊 Funcionalidades Avanzadas

### 1. Gráficos de Evolución
- Visualización en tiempo real
- Múltiples parámetros simultáneamente
- Exportación a imagen/PDF
- Zoom e interactividad

### 2. Análisis de IA
- Detección automática de anomalías
- Alertas por valores críticos
- Recomendaciones basadas en patrones
- Predicción de tendencias

### 3. Reportes Profesionales
- Formato PDF imprimible
- Gráficos incluidos
- Datos históricos
- Firma digital

### 4. Sincronización Automática
- Backups programados
- Sincronización en tiempo real
- Recuperación ante desastres
- Versionado de datos

---

## 🤖 Asistente IA

### Capacidades:
- Responde preguntas médicas
- Proporciona información de salud
- Sugiere acciones
- Mantiene historial de conversación
- Integración con datos del sistema

### Ejemplo de Uso:
```
Usuario: "¿Cuáles son los valores normales de glucosa?"
IA: "Los valores normales de glucosa en ayunas están entre 70-100 mg/dL..."
```

---

## 📈 Estadísticas del Sistema

El dashboard principal muestra:
- Total de pacientes registrados
- Registros de datos clínicos
- Diagnósticos realizados
- Tratamientos en curso

---

## 🛠️ Personalización

### Agregar Nueva Especialidad Médica:
Edita `web_ia.py` en la sección de especialidades del endpoint de citas.

### Agregar Nuevo Tipo de Análisis:
Edita `templates/laboratorios.html` en el select de `analysisType`.

### Cambiar Colores del Sistema:
Modifica los valores de gradiente en los archivos HTML:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

---

## 📝 Licencia

Sistema Médico Inteligente - Código Propietario

---

## 💬 Soporte

Para problemas técnicos o sugerencias:
1. Revisa los logs del servidor
2. Verifica la conexión a base de datos
3. Asegúrate de que los módulos estén instalados correctamente

---

## 🎯 Roadmap Futuro

- [ ] Integración con sistemas hospitalarios
- [ ] App móvil nativa
- [ ] Telemedicina por video
- [ ] Integración con laboratorios reales
- [ ] Inteligencia artificial avanzada
- [ ] Machine Learning para diagnósticos
- [ ] Portal del paciente

---

**Última actualización:** Enero 2024  
**Versión:** 2.0 - Sistema Completo

¡Gracias por usar el Sistema Médico Inteligente! 🏥
