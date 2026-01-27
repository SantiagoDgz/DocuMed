# 🏥 INSTALACIÓN Y CONFIGURACIÓN DEL SISTEMA DE PACIENTES

## ✅ Requisitos Previos

Asegúrate de tener instalado:
- **Python 3.6 o superior**
- **Flask** (generalmente ya está instalado)
- Un navegador web moderno (Chrome, Firefox, Safari, Edge)

---

## 📥 Paso 1: Verificar Instalación de Python

Abre una terminal/PowerShell y ejecuta:

```bash
python --version
```

Si ves una versión 3.6 o superior, ¡está bien!

---

## 📦 Paso 2: Instalar Flask (si no lo tienes)

```bash
pip install flask
```

---

## 📁 Paso 3: Verificar Archivos

En la carpeta `c:\Users\Santi\Downloads\Nueva carpeta\` debes tener:

```
✅ web_ia.py                    (Backend principal)
✅ pacientes_db.py              (Base de datos de pacientes)
✅ templates/
   ✅ index.html                (Chat con IA)
   ✅ pacientes.html            (Gestión de pacientes)
```

---

## 🚀 Paso 4: Iniciar el Servidor

Abre PowerShell/Terminal en la carpeta del proyecto:

```bash
cd c:\Users\Santi\Downloads\Nueva\ carpeta
python web_ia.py
```

Deberías ver algo como:
```
==================================================
  🤖 IA Asistente Web - Servidor Iniciado
==================================================

  Abre tu navegador en: http://localhost:5000

  Presiona Ctrl+C para detener el servidor

```

---

## 🌐 Paso 5: Abrir en el Navegador

### Para Gestión de Pacientes:
Abre tu navegador y ve a:
```
http://localhost:5000/pacientes
```

### Para Chat con IA (Claudia):
```
http://localhost:5000/
```

---

## ✨ Primer Uso

1. **Abre** `http://localhost:5000/pacientes`
2. **Haz clic** en "➕ Registrar Paciente"
3. **Completa** el formulario con datos de ejemplo
4. **Haz clic** en "💾 Guardar Paciente"
5. **Listo!** El paciente ha sido registrado

---

## 🧪 Prueba la Funcionalidad Completa (Opcional)

Si quieres verificar que todo funciona antes de usarlo:

```bash
python test_pacientes.py
```

Esto agregará un paciente de prueba y verificará todas las funciones.

---

## 🔧 Solución de Problemas

### **Error: "ModuleNotFoundError: No module named 'flask'"**
Solución:
```bash
pip install flask
```

### **Error: "Port 5000 already in use"**
El puerto 5000 ya está siendo usado. Opciones:
1. Cierra otras aplicaciones que usen el puerto
2. Usa otro puerto: `python web_ia.py` (modifica el código para puerto diferente)

### **Error: "ModuleNotFoundError: No module named 'pacientes_db'"**
Verificar que `pacientes_db.py` esté en la MISMA carpeta que `web_ia.py`

### **El navegador no carga la página**
- Espera 2-3 segundos después de ejecutar el comando
- Verifica que la URL sea exacta: `http://localhost:5000/pacientes`
- Recarga la página (F5 o Ctrl+R)

### **No puedo guardar pacientes**
- Verifica que tienes permisos de escritura en la carpeta
- En Windows, intenta ejecutar PowerShell como Administrador
- Asegúrate que el archivo `pacientes.json` no esté bloqueado

---

## 📱 Acceso desde Otros Dispositivos

### En la Misma Red (Tablet, Móvil, otra PC)

1. **Abre PowerShell en la PC servidor** y ejecuta:
```bash
ipconfig
```

2. **Busca "IPv4 Address"** (algo como: 192.168.1.100)

3. **En el otro dispositivo**, abre en el navegador:
```
http://192.168.1.100:5000/pacientes
```

---

## 📊 Estructura de Datos

Los datos se guardan automáticamente en **`pacientes.json`**:

```json
{
  "00001": {
    "id": "00001",
    "nombre": "Juan",
    "apellido": "Pérez",
    "cedula": "12345678",
    ...datos del paciente...
    "notas": [
      {
        "fecha": "2024-01-26 10:35:00",
        "contenido": "Nota de consulta..."
      }
    ]
  }
}
```

---

## 💾 Hacer Backup de Datos

Es importante hacer respaldo de tus datos:

**Opción 1: Manual**
- Localiza `pacientes.json`
- Cópialo a una carpeta segura o nube (Google Drive, OneDrive, etc.)

**Opción 2: Automático (próximamente)**
- Se puede configurar para hacer backup automático en nube

---

## 🔒 Seguridad Básica

### Para Uso Local/Personal:
✅ El sistema actual es seguro para:
- Consultorio privado
- Práctica médica pequeña
- Datos de prueba

### Para Hospital/Clínica:
⚠️ Se recomienda agregar:
- Autenticación de usuarios
- Contraseña para acceso
- Encriptación de datos
- Cumplimiento de HIPAA/GDPR
- Auditoría de cambios

---

## 🎓 Uso de la Interfaz

### Registrar Paciente
1. Pestaña "➕ Registrar Paciente"
2. Completa los campos
3. Botón "💾 Guardar Paciente"

### Ver Pacientes
1. Pestaña "📋 Ver Pacientes"
2. Ver tarjetas con información resumida
3. Botones: Ver, Editar, Eliminar

### Ver Detalles
1. Clic en "👁️ Ver" en cualquier tarjeta
2. Se abre modal con información completa
3. Ver historial de notas
4. Agregar nuevas notas

### Buscar
1. Pestaña "🔍 Buscar Paciente"
2. Escribe nombre, apellido o cédula
3. Clic en "🔍 Buscar"
4. Ver resultados

---

## ⏹️ Detener el Servidor

En la terminal/PowerShell donde corre el servidor:

```
Presiona: Ctrl + C
```

Verás:
```
Keyboard Interrupt
```

El servidor se habrá detenido.

---

## 🔄 Reiniciar el Servidor

Después de detenerlo:

```bash
python web_ia.py
```

Los datos se mantienen en `pacientes.json`, así que no se pierden.

---

## 🎯 Casos de Uso Comunes

### Caso 1: Médico con 50+ pacientes
✅ Sistema perfecto
- Registra cada paciente
- Ve la lista completa
- Busca rápidamente
- Agrega notas después de cada consulta

### Caso 2: Clínica con múltiples médicos
⚠️ Considera:
- Agregar login por usuario
- Permisos de acceso
- Auditoría de cambios

### Caso 3: Hospital grande
⚠️ Necesitas:
- Sistema profesional (Historia Clínica Electrónica)
- Certificación HIPAA/GDPR
- Bases de datos robustas
- Soporte técnico

---

## 📞 Soporte Rápido

**Problema**: Página no carga
**Solución**: Verifica la URL, espera unos segundos, recarga

**Problema**: No puedo guardar pacientes
**Solución**: Reinicia el servidor y el navegador

**Problema**: Datos desaparecieron
**Solución**: Revisa que `pacientes.json` exista en la carpeta

**Problema**: "Address already in use"
**Solución**: Cierra el servidor anterior (Ctrl+C) o cambia puerto

---

## ✅ Checklist de Instalación

- [ ] Python 3.6+ instalado
- [ ] Flask instalado
- [ ] Carpeta del proyecto lista
- [ ] `web_ia.py` presente
- [ ] `pacientes_db.py` presente
- [ ] `templates/pacientes.html` presente
- [ ] Servidor inicia sin errores
- [ ] Navegador carga `http://localhost:5000/pacientes`
- [ ] Puedo registrar un paciente
- [ ] Puedo ver la lista de pacientes
- [ ] Puedo agregar notas

---

**¡Listo para usar!** 🎉

Si tienes problemas, revisa el archivo `PACIENTES_GUIA.md` o `RESUMEN_IMPLEMENTACION.md`
