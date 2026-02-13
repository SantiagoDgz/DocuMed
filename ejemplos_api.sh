#!/bin/bash
# ejemplos_api.sh - Ejemplos de uso de la API IA Médica Profesional

# CONFIGURACIÓN
API_URL="http://localhost:5000"

echo "╔════════════════════════════════════════════════════════╗"
echo "║    EJEMPLOS DE USO API - IA MÉDICA PROFESIONAL         ║"
echo "╚════════════════════════════════════════════════════════╝"

# 1. VERIFICAR ESTADO
echo -e "\n📊 TEST 1: Verificar Estado de la IA"
echo "─────────────────────────────────────"
curl -s -X GET "$API_URL/api/medical/estado" | jq .

# 2. BUSCAR PACIENTE
echo -e "\n\n🔍 TEST 2: Buscar Paciente por Nombre"
echo "─────────────────────────────────────"
curl -s -X POST "$API_URL/api/medical/buscar-paciente" \
  -H "Content-Type: application/json" \
  -d '{"criterio": "nombre", "valor": "Juan"}' | jq .

# 3. OBTENER PERFIL PACIENTE
echo -e "\n\n👤 TEST 3: Obtener Perfil de Paciente"
echo "─────────────────────────────────────"
curl -s -X GET "$API_URL/api/medical/perfil-paciente/pac001" | jq .

# 4. ANALIZAR LABORATORIO
echo -e "\n\n🧪 TEST 4: Analizar Resultados de Laboratorio"
echo "─────────────────────────────────────────────────"
curl -s -X POST "$API_URL/api/medical/analizar-laboratorio" \
  -H "Content-Type: application/json" \
  -d '{
    "paciente_id": "pac001",
    "resultados": {
      "glucosa": 280,
      "hemoglobina": 9.5,
      "creatinina": 1.8,
      "presion_sistolica": 165
    }
  }' | jq .

# 5. OBTENER ALERTAS
echo -e "\n\n⚠️  TEST 5: Obtener Alertas del Paciente"
echo "────────────────────────────────────────"
curl -s -X GET "$API_URL/api/medical/alertas/pac001?solo_activas=true" | jq .

# 6. GENERAR ALERTA MANUAL
echo -e "\n\n🚨 TEST 6: Generar Alerta Manual"
echo "─────────────────────────────────"
curl -s -X POST "$API_URL/api/medical/generar-alerta" \
  -H "Content-Type: application/json" \
  -d '{
    "paciente_id": "pac001",
    "tipo": "interaccion_medicamento",
    "descripción": "Paciente alérgico a penicilina",
    "severidad": "CRÍTICO"
  }' | jq .

# 7. REGISTRAR CONSULTA
echo -e "\n\n📝 TEST 7: Registrar Consulta Médica"
echo "─────────────────────────────────────"
curl -s -X POST "$API_URL/api/medical/registrar-consulta" \
  -H "Content-Type: application/json" \
  -d '{
    "paciente_id": "pac001",
    "notas_médico": "Paciente con glucosa elevada y presión alta",
    "diagnóstico": "Diabetes descontrolada + Hipertensión",
    "recomendaciones": "Aumentar metformina a 1000mg. Añadir amlodipino 5mg."
  }' | jq .

# 8. OBTENER RESUMEN CLÍNICO
echo -e "\n\n📊 TEST 8: Obtener Resumen Clínico"
echo "───────────────────────────────────"
curl -s -X GET "$API_URL/api/medical/resumen-clínico/pac001" | jq .

# 9. COMPARAR ANÁLISIS TEMPORALES
echo -e "\n\n📈 TEST 9: Comparar Análisis Temporales"
echo "────────────────────────────────────────"
curl -s -X GET "$API_URL/api/medical/comparar-análisis/pac001?últimos=5" | jq .

# 10. CONSULTAR CON GROQ
echo -e "\n\n💬 TEST 10: Consultar con Groq AI"
echo "──────────────────────────────────"
curl -s -X POST "$API_URL/api/medical/consultar-groq" \
  -H "Content-Type: application/json" \
  -d '{
    "consulta": "¿Qué hacer con una glucosa de 280 en un paciente diabético?",
    "contexto": "Paciente diabético tipo 2, edad 65, medicado con metformina"
  }' | jq .

echo -e "\n\n╔════════════════════════════════════════════════════════╗"
echo "║           ✓ EJEMPLOS COMPLETADOS                        ║"
echo "╚════════════════════════════════════════════════════════╝"

echo -e "\n📌 NOTA: Asegúrate de que el servidor está corriendo en $API_URL"
echo "   Para iniciar: python web_ia.py"
