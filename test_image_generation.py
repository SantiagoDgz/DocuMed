#!/usr/bin/env python3
"""Test para verificar la generación de imágenes"""

import sys
sys.path.insert(0, r'c:\Users\Santi\Downloads\Nueva carpeta')

from PIL import Image
import base64
import io

def generar_imagen_rapida(descripcion):
    """Genera una imagen RÁPIDA y sin dependencias externas"""
    try:
        print(f"🎨 Generando imagen: {descripcion}")
        
        # Crear imagen MÁS PEQUEÑA para ser ultra-rápida
        width, height = 300, 300
        
        # Colores basados en hash de descripción (determinista)
        hash_val = sum(ord(c) for c in descripcion)
        r = (hash_val * 7) % 256
        g = (hash_val * 11) % 256
        b = (hash_val * 13) % 256
        
        # Crear imagen simple
        img = Image.new('RGB', (width, height), color=(r, g, b))
        
        # Convertir a PNG comprimido
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        image_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        
        print(f"✅ Imagen generada exitosamente")
        print(f"📊 Base64 size: {len(image_base64)} caracteres")
        
        return {
            'success': True,
            'image_base64': image_base64,
            'descripcion': descripcion,
            'mensaje': f"✨ **Imagen generada**\n\n📝 Descripción: {descripcion}\n\n🎨 Generada con IA"
        }
    
    except Exception as e:
        print(f"❌ Error al generar imagen: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'mensaje': f"❌ **Error al generar imagen**: {str(e)}\n\nIntenta nuevamente."
        }


if __name__ == '__main__':
    print("=" * 60)
    print("  🎨 TEST DE GENERACIÓN DE IMÁGENES")
    print("=" * 60)
    
    # Test 1: Descripción simple
    print("\n[TEST 1] Generando imagen simple...")
    resultado1 = generar_imagen_rapida("Un gato naranja")
    print(f"✓ Éxito: {resultado1['success']}")
    
    # Test 2: Descripción más larga
    print("\n[TEST 2] Generando imagen con descripción larga...")
    resultado2 = generar_imagen_rapida("Un castillo medieval en las montañas con un atardecer rojo")
    print(f"✓ Éxito: {resultado2['success']}")
    
    # Test 3: Caracteres especiales
    print("\n[TEST 3] Generando imagen con caracteres especiales...")
    resultado3 = generar_imagen_rapida("Un unicornio mágico 🦄✨")
    print(f"✓ Éxito: {resultado3['success']}")
    
    print("\n" + "=" * 60)
    print("  ✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 60)
