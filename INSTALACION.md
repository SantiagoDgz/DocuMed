🚀 GUÍA DE INSTALACIÓN - IA MÉDICA PROFESIONAL
═══════════════════════════════════════════════════════

## REQUISITOS PREVIOS

- Python 3.8 o superior
- pip (gestor de paquetes)
- API Key de Groq (ya configurada en web_ia.py)

═══════════════════════════════════════════════════════

## PASO 1: Instalar Dependencias

### Windows PowerShell:
```
pip install -r requirements.txt
```

### O manualmente:
```
pip install flask>=2.3.0
pip install groq>=0.4.1
pip install python-dotenv>=1.0.0
```

═══════════════════════════════════════════════════════

## PASO 2: Verificar API Key de Groq

Abre web_ia.py y verifica que la API key esté:

```python
GROQ_API_KEY = "TU_API_KEY_AQUI"
```

Si NO está, obtenerla aquí: https://console.groq.com/keys

═══════════════════════════════════════════════════════

## PASO 3: Correr Pruebas

```bash
python test_ia_medica.py
```

Debe mostrar:
✓ PRUEBAS COMPLETADAS
✓ Búsqueda de pacientes
✓ Análisis de laboratorio
✓ Generación de alertas
✓ Perfiles de pacientes

═══════════════════════════════════════════════════════

## PASO 4: Iniciar Servidor

```bash
python web_ia.py
```

Verás:
 * Running on http://127.0.0.1:5000

═══════════════════════════════════════════════════════

## PASO 5: Probar API

En otra terminal/cmd, ejecuta:

```bash
# Verificar estado
curl http://localhost:5000/api/medical/estado

# Buscar paciente
curl -X POST http://localhost:5000/api/medical/buscar-paciente ^
  -H "Content-Type: application/json" ^
  -d "{\"criterio\": \"nombre\", \"valor\": \"Juan\"}"
```

═══════════════════════════════════════════════════════

## ESTRUCTURA DE ARCHIVOS NECESARIOS

✓ medical_ai.py - IA
✓ web_ia.py - Server Flask/Groq
✓ medical_ia_routes.py - Rutas API
✓ test_ia_medica.py - Pruebas
✓ requirements.txt - Dependencias
✓ datos_medicos.json - BD (se crea)
✓ pacientes_db.json - BD (se crea)

═══════════════════════════════════════════════════════

## SOLUCIÓN DE PROBLEMAS

### "ModuleNotFoundError: No module named 'flask'"
→ pip install flask

### "API Key de Groq no válida"
→ Verifica en https://console.groq.com/keys
→ Reemplaza en web_ia.py línea 16

### "Puerto 5000 ya en uso"
→ Cierra otros procesos en ese puerto
→ O cambia puerto en web_ia.py

### "No puedo importar groq"
→ pip install groq

═══════════════════════════════════════════════════════

## USO DESDE PYTHON

```python
from medical_ai import IAMedicaProfesional

ia = IAMedicaProfesional()

# Buscar paciente
resultados = ia.buscar_paciente('nombre', 'Juan')

# Analizar laboratorio
análisis = ia.analizar_resultados_laboratorio('pac001', {
    'glucosa': 280,
    'hemoglobina': 9.5
})

# Ver alertas
alertas = ia.obtener_alertas_paciente('pac001')

print(alertas)
```

═══════════════════════════════════════════════════════

## PRÓXIMOS PASOS

1. Instalar y ejecutar
2. Crear pacientes en pacientes_db.json
3. Subir resultados de laboratorio
4. El sistema alerta automáticamente
5. Revisar con Groq si es necesario

═══════════════════════════════════════════════════════

¿Necesitas ayuda?
- Lee IA_MEDICA_PROFESIONAL.md
- Ejecuta python test_ia_medica.py
- Verifica ejemplos_api.sh

════════════════════════════════════════════════════════
