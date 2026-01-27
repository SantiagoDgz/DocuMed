# 🏥 SISTEMA DE GESTIÓN DE PACIENTES - INICIO RÁPIDO

## ⚡ En 3 pasos

### 1. Inicia el servidor
```bash
python web_ia.py
```

### 2. Abre en tu navegador
```
http://localhost:5000/pacientes
```

### 3. ¡Comienza a registrar pacientes!

---

## 📋 Lo que puedes hacer

✅ **Registrar pacientes** - Nombre, edad, cédula, información médica completa
✅ **Ver lista de pacientes** - Tarjetas con información resumida
✅ **Buscar pacientes** - Por nombre, apellido o cédula
✅ **Ver detalles completos** - Toda la información del paciente
✅ **Agregar notas** - Notas de cada consulta con fecha/hora automática
✅ **Eliminar pacientes** - Con confirmación de seguridad

---

## 📁 Archivos Nuevos

```
pacientes_db.py      ← Base de datos (gestión de datos)
pacientes.html       ← Interfaz web (donde escribes datos)
PACIENTES_GUIA.md    ← Guía completa de uso
test_pacientes.py    ← Script para probar todo
```

---

## 🧪 Prueba Todo (Opcional)

Si quieres verificar que todo funciona antes de usar:

```bash
python test_pacientes.py
```

Esto agregará un paciente de prueba y verificará que todo esté bien.

---

## 🔧 Requisitos

- Python 3.6+
- Flask (ya instalado)
- Navegador web moderno

---

## ❓ Problemas comunes

**"ModuleNotFoundError: No module named 'pacientes_db'"**
→ Asegúrate que `pacientes_db.py` esté en la MISMA carpeta que `web_ia.py`

**"Puerto 5000 en uso"**
→ Usa otro puerto: `python web_ia.py --port 5001`

**"No puedo guardar pacientes"**
→ Verifica permisos de escritura en la carpeta

---

## 📱 Acceso desde otro dispositivo

1. En tu PC abre: `ipconfig` (Windows) o `ifconfig` (Mac/Linux)
2. Copia tu IP local (ej: 192.168.1.100)
3. Desde otro dispositivo abre: `http://192.168.1.100:5000/pacientes`

---

## 🎓 Próximas características

- Edición directa de pacientes
- Gráficos de seguimiento médico
- Exportar datos (PDF, Excel, CSV)
- Autenticación y permisos
- App móvil

---

**¡Listo! Tu médico ya puede empezar a gestionar pacientes.** 👨‍⚕️✨
