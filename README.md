# DocuMed

Sistema integral de gestión médica con inteligencia artificial, potenciado por API Groq (Llama 3.3).

## Características Principales

### Sistema de Pacientes
- Registro y gestión completa de pacientes
- Búsqueda avanzada por ID o nombre
- Edición y eliminación de registros
- Base de datos SQLite integrada
- Historial médico detallado

### Panel Médico Inteligente
- Chat con IA médica en tiempo real
- Análisis de síntomas y diagnósticos
- Recomendaciones médicas personalizadas
- Información sobre medicamentos y tratamientos
- Interfaz conversacional amigable

### Gestión de Citas
- Programación de citas médicas
- Sistema de calendario integrado
- Recordatorios automáticos
- Historial de citas

### Análisis de Laboratorio
- Carga de resultados de laboratorio
- Visualización de pruebas clínicas
- Seguimiento de valores normales
- Gráficas de histórico

### Recetas Digitales
- Emisión de prescripciones digitales
- Listado de medicamentos
- Dosificación y duración
- Archivo de recetas históricas

### Seguridad y Privacidad
- Encriptación AES-128 de datos sensibles
- Autenticación de usuarios
- Sincronización segura en la nube
- Backup automático de datos
- Gestión de claves maestras

## Alcance Simplificado (MVP)

Esta versión prioriza un flujo **simple y práctico** para uso personal del médico:

- **Expediente digital básico**: pacientes, historial, diagnósticos, tratamientos y notas.
- **Búsqueda rápida** y organización por fecha/tipo.
- **Asistente IA** para resúmenes y alertas simples (sin reemplazar el criterio clínico).
- **Ejecución local** con configuración mínima.

### Fuera de alcance (por ahora)
- Cumplimiento normativo avanzado (HIPAA/LOPD/GDPR).
- Múltiples usuarios con roles y auditoría.
- Integraciones complejas con sistemas hospitalarios.

> Nota: El objetivo es reducir complejidad inicial y enfocarse en productividad personal.

## Tecnologías Utilizadas

- **Backend:** Python 3 con Flask
- **Frontend:** HTML5, CSS3, JavaScript vanilla
- **IA:** Groq API (Modelo Llama 3.3)
- **Base de Datos:** SQLite
- **Seguridad:** Encriptación AES-128

## Instalación

### Requisitos
- Python 3.8+
- pip
- Conexión a internet

### Pasos

1. Clonar el repositorio:
\\\ash
git clone https://github.com/SantiagoDgz/DocuMed.git
cd DocuMed
\\\

2. Instalar dependencias:
\\\ash
pip install -r requirements.txt
\\\

3. Ejecutar:
\\\ash
python launcher.py
\\\

O en Windows:
\\\ash
.\run_server.bat
\\\

4. Acceder en: http://localhost:5000
   - Usuario: admin
   - Contraseña: admin123

## Estructura del Proyecto

- launcher.py - Punto de entrada
- web_ia_simple.py - Servidor Flask
- medical_ai.py - Análisis médico
- pacientes_db.py - Base de datos
- encryption.py - Encriptación
- cloud_sync.py - Sincronización
- templates/ - Plantillas HTML

## Características

- Gestión de pacientes
- Chat médico con IA
- Citas y calendario
- Laboratorios
- Recetas digitales
- Seguridad y encriptación
- Backups automáticos

## Credenciales Demo

Usuario: admin
Contraseña: admin123

## API

- GET /api/pacientes
- POST /api/pacientes
- GET /api/chat
- POST /api/chat

## Licencia

MIT License

## Autor

SantiagoDgz

---

DocuMed - Sistema de Gestión Médica Inteligente
Potenciado por Groq API (Llama 3.3)
