#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para agregar header profesional a todos los HTML"""

import os
import re
from pathlib import Path

# Header HTML profesional
HEADER_HTML = '''    <!-- Professional Top Header -->
    <header class="top-header">
        <a href="/home" class="logo-brand">
            <img src="/static/images/logo.png" alt="DocuMed" class="logo-img">
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
            background: linear-gradient(135deg, #667eea 0%, #482d97 100%);
            color: white;
            padding: 15px 30px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
            border-bottom: 3px solid #764ba2;
        }
        
        .logo-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: white;
        }
        
        .logo-img {
            width: 40px;
            height: 40px;
            border-radius: 6px;
            object-fit: contain;
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
        
        .main-content {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
'''

# Body styles para flexbox
BODY_STYLE_OLD = 'body {\n            font-family:'
BODY_STYLE_NEW = '''body {
            font-family:'''

TEMPLATES_DIR = Path("templates")
FILES_TO_UPDATE = [
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
        # Si no tiene style, crear uno (raro pero posible)
        elif '</head>' in content:
            style_section = '<style>' + HEADER_CSS + '\n    </style>'
            content = content.replace('</head>', style_section + '\n</head>', 1)
    
    # Buscar <body> e insertar header
    if '<body>' in content:
        content = content.replace('<body>', '<body>\n' + HEADER_HTML, 1)
        
        # Buscar </body> y agregar cierre de main-content
        if '</body>' in content:
            content = content.replace('</body>', '    </div>\n</body>', 1)
        
        # Actualizar body para flexbox si no lo tiene
        if 'display: flex;' not in content.split('<body>')[0]:
            # Buscar la definición de body en style y actualizar
            pattern = r'body\s*\{([^}]*?)padding:\s*20px;'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    'body {\n            font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif;\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            min-height: 100vh;\n            display: flex;\n            flex-direction: column;\n            padding: 0;',
                    content,
                    count=1,
                    flags=re.DOTALL
                )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filepath.name} - Header agregado")
        return True
    else:
        print(f"❌ {filepath.name} - No se encontró <body>")
        return False

def main():
    """Procesa todos los archivos HTML"""
    print("🔄 Agregando headers profesionales...\n")
    
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
