#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image
from collections import Counter

# Abrir imagen
img = Image.open('img/logo.png')
img = img.convert('RGB')

# Redimensionar para análisis más rápido
img.thumbnail((200, 200))

# Obtener todos los píxeles y filtrar negros/grises oscuros
pixels = []
for p in img.getdata():
    # Filtrar píxeles muy oscuros (probablemente fondo)
    if not (p[0] < 30 and p[1] < 30 and p[2] < 30):
        pixels.append(p)

if pixels:
    # Contar colores más frecuentes
    color_counts = Counter(pixels)
    most_common = color_counts.most_common(10)
    
    print("🎨 Colores principales del logo (excluyendo negros):")
    colors_output = []
    for i, (rgb, count) in enumerate(most_common, 1):
        hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
        colors_output.append(hex_color)
        print(f"{i}. RGB{rgb} = {hex_color} ({count} píxeles)")
    
    # Guardar colores
    with open('logo_colors.txt', 'w') as f:
        for color in colors_output[:3]:
            f.write(color + '\n')
    print("\n✅ Colores principales guardados")
else:
    print("⚠️ Logo parece ser principalmente negro/oscuro")
    print("Usando colores DocuMed por defecto...")
    colors = ['#667eea', '#764ba2', '#482d97']
    with open('logo_colors.txt', 'w') as f:
        for color in colors:
            f.write(color + '\n')
