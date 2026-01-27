#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import requests
import json
import time

print("="*60)
print("  TEST DE SERVIDOR - Generacion de Imagenes")
print("="*60)

time.sleep(2)

# Test 1: Generar imagen via endpoint directo
print("\n[TEST 1] Via /generar-imagen")
try:
    r = requests.post('http://127.0.0.1:5000/generar-imagen', 
        json={'descripcion': 'Un gato naranja'},
        timeout=10
    )
    print(f"  Status: {r.status_code}")
    data = r.json()
    print(f"  Success: {data.get('success')}")
    if data.get('imagen_base64'):
        print(f"  Imagen size: {len(data.get('imagen_base64'))} chars")
except Exception as e:
    print(f"  ERROR: {e}")

# Test 2: Generar imagen via chat
print("\n[TEST 2] Via /chat (generate image)")
try:
    r = requests.post('http://127.0.0.1:5000/chat',
        json={'mensaje': 'genera imagen de un castillo'},
        timeout=10
    )
    print(f"  Status: {r.status_code}")
    data = r.json()
    print(f"  es_imagen: {data.get('es_imagen')}")
    if data.get('imagen_base64'):
        print(f"  Imagen size: {len(data.get('imagen_base64'))} chars")
    print(f"  Respuesta: {str(data.get('respuesta', ''))[:60]}...")
except Exception as e:
    print(f"  ERROR: {e}")

# Test 3: Mensaje normal
print("\n[TEST 3] Mensaje normal")
try:
    r = requests.post('http://127.0.0.1:5000/chat',
        json={'mensaje': 'Cual es tu nombre'},
        timeout=10
    )
    print(f"  Status: {r.status_code}")
    data = r.json()
    print(f"  Respuesta: {str(data.get('respuesta', ''))[:60]}...")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "="*60)
print("  TESTS COMPLETADOS")
print("="*60)
