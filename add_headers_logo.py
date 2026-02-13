#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para agregar header profesional con logo PNG a todos los HTML"""

import os
import re
from pathlib import Path

# Header HTML profesional
HEADER_HTML = '''    <!-- Professional Top Header -->
    <header class="top-header">
        <a href="/home" class="logo-brand">
            <img src="/img/hvirfill logo.jpg" alt="DocuMed" class="logo-img">
            <div class="brand-info">
                <h2>DocuMed</h2>
                <p>Sistema Médico Inteligente</p>
            </div>
        </a>
    </header>
    
    <div class="main-content">
'''

HEADER_CSS = '''
        .top-header {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #482d97 100%);
            color: white;
            padding: 15px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
            border-bottom: 3px solid #764ba2;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
        }
        
        .logo-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: white;
        }
        
        .logo-img {
            height: 50px;
            width: auto;
            border-radius: 6px;
            object-fit: contain;
            background: rgba(255,255,255,0.1);
            padding: 4px 8px;
        }
        
        .brand-info h2 {
            margin: 0;
            font-size: 20px;
            font-weight: bold;
        }
        
        .brand-info p {
            margin: 0;
            font-size: 11px;
            opacity: 0.9;
        }
        
        body {
            padding-top: 80px;
        }
        
        .main-content {
            flex: 1;
            width: 100%;
        }
'''

TEMPLATES_DIR = Path("templates")
FILES_TO_UPDATE = [
    "home.html",
    "dashboard.html",
    "pacientes.html",
    "laboratorios.html",
    "citas.html",
    "recetas.html",
    "captura_datos.html",
    "analisis_reportes.html",
    "seguridad.html",
    "test.html"
]

def add_header_to_file(filepath):
    """Agrega header profesional a un archivo HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Si ya tiene header, saltarlo
    if 'class="top-header"' in content:
        print(f"⏭️  {filepath.name} - Ya tiene header")
        return False
    
    # Insertar CSS si no lo tiene
    if '.top-header' not in content:
        # Buscar </style> para insertar CSS antes
        if '</style>' in content:
            content = content.replace('</style>', HEADER_CSS + '\n    </style>', 1)
    
    # Buscar <body> e insertar header
    if '<body>' in content:
        content = content.replace('<body>', '<body>\n' + HEADER_HTML, 1)
        
        # Buscar </body> y agregar cierre de main-content
        if '</body>' in content:
            content = content.replace('</body>', '    </div>\n</body>', 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filepath.name} - Header agregado")
    return True

def main():
    """Procesa todos los archivos HTML"""
    print("🔄Agregando headers profesionales con logo PNG...\n")
    
    updated = 0
    for filename in FILES_TO_UPDATE:
        filepath = TEMPLATES_DIR / filename
        if filepath.exists():
            if add_header_to_file(filepath):
                updated += 1
        else:
            print(f"⚠️  {filename} - No encontrado")
    
    print(f"\n✨ Completado: {updated}/{len(FILES_TO_UPDATE)} archivos actualizados")

if __name__ == '__main__':
    main()
