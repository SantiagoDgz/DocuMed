#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de verificación rápida - Generador de Imágenes
Verifica que todos los módulos necesarios estén instalados
"""

import sys
import os

def verificar_imports():
    """Verifica que todos los imports necesarios funcionan"""
    print("🔍 Verificando imports necesarios...\n")
    
    imports_requeridos = [
        ('flask', 'Flask'),
        ('groq', 'Groq'),
        ('PIL', 'Pillow (PIL)'),
        ('requests', 'requests'),
        ('base64', 'base64 (built-in)'),
    ]
    
    errores = []
    
    for modulo, nombre in imports_requeridos:
        try:
            __import__(modulo)
            print(f"✅ {nombre:<30} - OK")
        except ImportError as e:
            print(f"❌ {nombre:<30} - FALTA")
            errores.append((nombre, str(e)))
    
    print("\n" + "="*50)
    
    if errores:
        print("⚠️  Faltan dependencias:")
        for nombre, error in errores:
            print(f"   - {nombre}")
        print("\n📦 Instálalas con:")
        print("   pip install Pillow requests groq flask")
        return False
    else:
        print("✅ Todas las dependencias están instaladas!")
        return True

def verificar_archivos():
    """Verifica que los archivos principales existan"""
    print("\n🔍 Verificando archivos principales...\n")
    
    archivos = [
        'web_ia_simple.py',
        'templates/index.html',
        'GENERADOR_IMAGENES.md',
        'GUIA_RAPIDA_IMAGENES.md',
        'CAMBIOS_IMPLEMENTADOS.md',
    ]
    
    para_crear = []
    
    for archivo in archivos:
        if os.path.exists(archivo):
            print(f"✅ {archivo:<40} - EXISTS")
        else:
            print(f"❌ {archivo:<40} - MISSING")
            para_crear.append(archivo)
    
    print("\n" + "="*50)
    
    if para_crear:
        print(f"⚠️  Faltan {len(para_crear)} archivo(s):")
        for archivo in para_crear:
            print(f"   - {archivo}")
        return False
    else:
        print("✅ Todos los archivos necesarios existen!")
        return True

def verificar_contenido():
    """Verifica que el contenido principal esté en los archivos"""
    print("\n🔍 Verificando contenido de archivos...\n")
    
    # Verificar que web_ia_simple.py tiene la función generar_imagen
    with open('web_ia_simple.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
        
        checks = [
            ('generar_imagen' in contenido, "Método generar_imagen()"),
            ('@app.route' in contenido, "Rutas Flask"),
            ('IAClaudia' in contenido, "Clase IAClaudia"),
            ("'/generar-imagen'" in contenido, "Ruta /generar-imagen"),
            ('Hugging Face' in contenido, "API Hugging Face"),
        ]
        
        for existe, nombre in checks:
            status = "✅" if existe else "❌"
            print(f"{status} {nombre:<40}")
    
    # Verificar que index.html tiene las funciones nuevas
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        contenido = f.read()
        
        checks = [
            ('agregarMensajeConImagen' in contenido, "Función agregarMensajeConImagen"),
            ('abrirGeneradorImagenes' in contenido, "Función abrirGeneradorImagenes"),
            ('generar-imagen' in contenido, "Endpoint /generar-imagen"),
            ('image-container' in contenido, "Estilos para imágenes"),
            ('🎨 Generar Imagen' in contenido, "Botón de generar imágenes"),
        ]
        
        for existe, nombre in checks:
            status = "✅" if existe else "❌"
            print(f"{status} {nombre:<40}")
    
    print("\n" + "="*50)
    print("✅ Verificación de contenido completa!")
    return True

def main():
    """Ejecuta todas las verificaciones"""
    print("="*50)
    print("🎨 Verificación - Generador de Imágenes")
    print("="*50)
    print()
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Ejecutar verificaciones
    imports_ok = verificar_imports()
    archivos_ok = verificar_archivos()
    verificar_contenido()
    
    print("\n" + "="*50)
    print("📋 RESUMEN")
    print("="*50)
    
    if imports_ok and archivos_ok:
        print("""
✅ ¡LISTO PARA USAR!

Para iniciar la aplicación:
    python web_ia_simple.py

Luego abre en tu navegador:
    http://localhost:5000

🎨 Para generar imágenes:
    1. Click en el botón "🎨 Generar Imagen"
    2. Escribe una descripción
    3. ¡Espera a que la IA genere tu imagen!
        """)
    else:
        print("""
⚠️  FALTAN AJUSTES

Por favor:
1. Instala los módulos faltantes
2. Verifica que todos los archivos existan
3. Intenta nuevamente
        """)
    
    return 0 if (imports_ok and archivos_ok) else 1

if __name__ == '__main__':
    sys.exit(main())
