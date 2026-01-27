#!/usr/bin/env python3
"""Test para verificar la generación de imágenes via chat"""

import requests
import json

# Detener servidor anterior si está corriendo
import subprocess
import time

print("=" * 60)
print("  🧪 TEST DE GENERACIÓN DE IMÁGENES VIA CHAT")
print("=" * 60)

time.sleep(2)

# Test 1: Via endpoint /generar-imagen
print("\n[TEST 1] Generar imagen via /generar-imagen")
try:
    response = requests.post('http://localhost:5000/generar-imagen', 
        json={'descripcion': 'Un gato naranja'},
        timeout=10
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Imagen_base64 length: {len(data.get('imagen_base64', ''))}")
    print(f"Mensaje: {data.get('mensaje', '')[:50]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Via endpoint /chat con palabra "genera imagen"
print("\n[TEST 2] Generar imagen via /chat (con 'genera imagen')")
try:
    response = requests.post('http://localhost:5000/chat',
        json={'mensaje': 'genera imagen de un castillo'},
        timeout=10
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"es_imagen: {data.get('es_imagen')}")
    print(f"imagen_base64 present: {'imagen_base64' in data}")
    if data.get('imagen_base64'):
        print(f"Imagen_base64 length: {len(data.get('imagen_base64'))}")
    print(f"Respuesta: {data.get('respuesta', '')[:80]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Via endpoint /chat con mensaje normal
print("\n[TEST 3] Mensaje normal via /chat")
try:
    response = requests.post('http://localhost:5000/chat',
        json={'mensaje': '¿Cuál es tu nombre?'},
        timeout=10
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"es_imagen: {data.get('es_imagen')}")
    print(f"Respuesta: {data.get('respuesta', '')[:80]}...")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("  ✅ TESTS COMPLETADOS")
print("=" * 60)
