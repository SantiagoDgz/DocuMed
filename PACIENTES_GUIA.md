# 👨‍⚕️ Sistema de Gestión de Pacientes - Guía Completa

## ¿Qué es esto?

Es un **sistema web completo** que permite a un médico **guardar, buscar y gestionar información de sus pacientes** de forma fácil y segura. Se integra perfectamente con tu IA Claudia.

---

## 📋 Características Principales

### ✅ Registro de Pacientes
- **Información Personal**: Nombre, Apellido, Cédula, Edad, Género, Teléfono, Email, Dirección
- **Información Médica**: Peso, Altura, Presión Arterial, Alergias, Medicamentos, Historia Médica
- **Seguimiento**: Fecha de última consulta y registro automático

### ✅ Gestión Completa
- **Ver Pacientes**: Visualiza todos los pacientes en tarjetas informativas
- **Buscar Pacientes**: Búsqueda rápida por nombre, apellido o cédula
- **Notas de Consulta**: Agrega notas a cada paciente después de cada consulta
- **Detalles Completos**: Acceso total a toda la información del paciente

### ✅ Eliminación y Control
- Elimina pacientes (con confirmación)
- Sistema de alertas para acciones importantes
- Interfaz intuitiva y responsiva

---

## 🚀 Cómo Usar

### 1️⃣ **Iniciar la Aplicación**

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python web_ia.py
```

Luego abre tu navegador en: **http://localhost:5000/pacientes**

---

### 2️⃣ **Registrar un Nuevo Paciente**

1. Haz clic en la pestaña **"➕ Registrar Paciente"**
2. Completa los campos (los marcados con * son obligatorios)
3. Haz clic en **"💾 Guardar Paciente"**

**Campos Disponibles:**
- **Información Personal**: Nombre, Apellido, Cédula, Edad, Género, Teléfono, Email, Dirección
- **Información Médica**: Peso, Altura, Presión Arterial, Alergias, Medicamentos, Historia Médica, Última Consulta

---

### 3️⃣ **Ver Lista de Pacientes**

1. Haz clic en **"📋 Ver Pacientes"**
2. Se mostrarán todas los pacientes en tarjetas
3. Cada tarjeta muestra:
   - Nombre completo
   - ID único
   - Información básica (edad, cédula, teléfono, peso)
   - Botones para: Ver detalles, Editar, Eliminar

---

### 4️⃣ **Ver Detalles de un Paciente**

1. Haz clic en el botón **"👁️ Ver"** en la tarjeta del paciente
2. Se abre un modal con:
   - **Información Personal**: Nombre, contacto, dirección
   - **Información Médica**: Peso, altura, presión, historial
   - **Notas de Consulta**: Historial de todas las notas
   - **Agregar Nueva Nota**: Formulario para añadir notas

---

### 5️⃣ **Agregar Notas de Consulta**

1. Abre los detalles de un paciente
2. Desplázate al final del modal
3. En la sección **"➕ Agregar Nota de Consulta"**:
   - Escribe la nota
   - Haz clic en **"💾 Guardar Nota"**
4. La nota se guardará con fecha y hora automática

---

### 6️⃣ **Buscar un Paciente**

1. Haz clic en **"🔍 Buscar Paciente"**
2. Escribe el nombre, apellido o cédula del paciente
3. Haz clic en **"🔍 Buscar"**
4. Se mostrarán los resultados encontrados

---

## 💾 ¿Dónde se Guardan los Datos?

Los datos se guardan automáticamente en un archivo **`pacientes.json`** en la misma carpeta del proyecto. Este archivo contiene:
- Información de todos los pacientes
- Notas de cada paciente
- Fechas de registro

**Importante:** Guarda regularmente este archivo como respaldo.

---

## 🔒 Seguridad

⚠️ **Nota**: Este sistema es local. Si necesitas:
- **Mayor seguridad**: Implementar contraseñas de acceso
- **Backup automático**: Hacer copias en la nube
- **Cumplir HIPAA**: Agregar autenticación y encriptación

Te recomendamos consultar con un especialista en privacidad médica.

---

## 📱 Acceso Multiplataforma

Puedes acceder desde:
- **PC**: http://localhost:5000/pacientes
- **Tablet**: Mismo enlace en la red local
- **Móvil**: Same network - http://TuIP:5000/pacientes

Para acceder desde otro dispositivo:
1. Abre una terminal y ejecuta `ipconfig` (Windows) o `ifconfig` (Mac/Linux)
2. Busca tu IP local (ejemplo: 192.168.1.100)
3. Accede desde otro dispositivo a: http://192.168.1.100:5000/pacientes

---

## 🛠️ Archivos Creados

```
├── pacientes_db.py          # Base de datos de pacientes
├── pacientes.html           # Interfaz web de gestión
├── pacientes.json          # Archivo de datos (se crea automáticamente)
└── web_ia.py               # Backend actualizado con rutas de pacientes
```

---

## 🔗 Integración con Claudia IA

También puedes acceder a la IA en: http://localhost:5000/

Ahora tienes dos servicios en tu servidor:
- **IA Chat**: http://localhost:5000/
- **Gestión de Pacientes**: http://localhost:5000/pacientes

---

## ❓ Preguntas Frecuentes

### ¿Cómo hago respaldo de los pacientes?
Descarga el archivo `pacientes.json` regularmente o usa un servicio de nube como Google Drive.

### ¿Puedo editar un paciente?
Actualmente puedes ver y agregar notas. Para editar, abre los detalles, copia la info, elimina y re-registra. Pronto agregaremos edición directa.

### ¿Qué pasa si cierro el navegador?
Los datos se guardan en el servidor. Puedes cerrar sin problemas.

### ¿Puedo acceder desde múltiples dispositivos?
Sí, siempre que estén en la misma red y el servidor esté ejecutándose.

### ¿Qué pasa si se reinicia la PC?
Los datos permanecen en `pacientes.json`. Solo necesitas reiniciar el servidor.

---

## 📞 Soporte

Si encuentras problemas:
1. Verifica que `pacientes_db.py` esté en la misma carpeta que `web_ia.py`
2. Revisa la consola para mensajes de error
3. Asegúrate de tener permisos de escritura en la carpeta
4. Intenta reiniciar el servidor

---

## 🎓 Próximas Mejoras

- ✏️ Edición directa de pacientes
- 📊 Gráficos de seguimiento médico
- 📧 Envío de recordatorios por email
- 📁 Importar/Exportar datos (CSV, Excel)
- 🔐 Autenticación y permisos de usuario
- 📱 App móvil nativa

---

**¡Listo para usar! Ahora tu médico puede gestionar pacientes fácilmente.** 👨‍⚕️✨
