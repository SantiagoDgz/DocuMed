# Sistema de Gestión de Pacientes - Archivo de Configuración

# Configuración básica
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# Configuración de la base de datos
DATABASE_FILE = 'pacientes.json'
AUTO_SAVE = True

# Información de la clínica/consultorio
CLINIC_NAME = "Consultorio Médico"
CLINIC_EMAIL = "contacto@consultorio.com"
CLINIC_PHONE = "+1-555-0000"

# Configuración de seguridad
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
SESSION_TIMEOUT = 3600  # 1 hora

# Configuración de pacientes
CAMPOS_OBLIGATORIOS = [
    'nombre',
    'apellido', 
    'cedula',
    'edad'
]

# Especialidades médicas
ESPECIALIDADES = [
    'Medicina General',
    'Cardiología',
    'Dermatología',
    'Pediatría',
    'Odontología',
    'Oftalmología',
    'Otorrinolaringología',
    'Neurología',
    'Psiquiatría',
    'Traumatología',
    'Ginecología',
    'Otro'
]

# Colores para la interfaz (puedes cambiar)
PRIMARY_COLOR = '#667eea'
SECONDARY_COLOR = '#764ba2'
SUCCESS_COLOR = '#51cf66'
DANGER_COLOR = '#ff6b6b'
WARNING_COLOR = '#ffd700'
INFO_COLOR = '#0c5460'

# Configuración de exportación
EXPORT_FORMAT = ['json', 'csv', 'pdf']
DEFAULT_EXPORT_FORMAT = 'json'

# Idioma
LANGUAGE = 'es'  # es = Español, en = English

# Zona horaria
TIMEZONE = 'America/Caracas'  # Cambiar según tu región
