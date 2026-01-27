#!/usr/bin/env python3
"""Script para iniciar el servidor sin interferencias de PowerShell"""
import subprocess
import sys
import time
import requests

# Detener procesos anteriores
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
time.sleep(2)

# Iniciar servidor en background
print("🚀 Iniciando servidor...")
proc = subprocess.Popen(
    [sys.executable, 'web_ia_simple.py'],
    cwd=r'c:\Users\Santi\Downloads\Nueva carpeta',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.DEVNULL
)

# Esperar a que inicie
time.sleep(5)

# Probar conexión
print("\n🧪 Probando conexión...")
try:
    r = requests.post('http://127.0.0.1:5000/chat', json={'mensaje': 'test'}, timeout=5)
    print(f"✅ Status: {r.status_code}")
    print(f"✅ Respuesta: {r.json()}")
    print("\n✨ ¡SERVIDOR FUNCIONANDO!")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n📋 Output del servidor:")
    stdout, stderr = proc.communicate(timeout=2)
    print(stdout.decode('utf-8', errors='ignore'))
    if stderr:
        print("Stderr:")
        print(stderr.decode('utf-8', errors='ignore'))

print("\nPresiona Ctrl+C para detener el servidor")
try:
    proc.wait()
except KeyboardInterrupt:
    print("\n⏹️  Deteniendo...")
    proc.terminate()
    proc.wait()
