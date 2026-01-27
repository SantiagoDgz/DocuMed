#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'ok', 'mensaje': 'Servidor funcionando'})

@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({'respuesta': 'Test OK', 'es_imagen': False})

@app.route('/generar-imagen', methods=['POST'])
def generar_imagen_route():
    return jsonify({'success': True, 'mensaje': 'Test OK', 'imagen_base64': 'TEST'})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  🤖 TEST SERVER - Iniciado")
    print("="*50)
    print("\n  Abre tu navegador en: http://localhost:5000")
    print("\n  Presiona Ctrl+C para detener el servidor\n")
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False, threaded=True)
