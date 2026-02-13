#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup_pacientes.py - Configura pacientes realistas

import json
from datetime import datetime, timedelta
from medical_ai import IAMedicaProfesional
import sys
import io

# Fijar encoding a UTF-8 para Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def crear_pacientes_realistas():
    """Crea pacientes con datos clínicos realistas"""
    ia = IAMedicaProfesional()
    
    # Paciente 1: Diabetes descontrolada con hipertensión
    pacientes = {
        'pac001': {
            'nombre': 'Juan',
            'apellido': 'García',
            'cedula': '12345678',
            'edad': 65,
            'genero': 'M',
            'email': 'juan@example.com',
            'telefono': '555-1234',
            'diagnósticos': ['Diabetes Tipo 2', 'Hipertensión', 'Dislipidemia'],
            'medicamentos': ['Metformina 1000mg c/12h', 'Losartán 50mg c/d', 'Atorvastatina 20mg c/d'],
            'alergias': 'Penicilina, AINES',
            'última_consulta': datetime.now().isoformat()
        },
        'pac002': {
            'nombre': 'María',
            'apellido': 'López',
            'cedula': '87654321',
            'edad': 48,
            'genero': 'F',
            'email': 'maria@example.com',
            'telefono': '555-5678',
            'diagnósticos': ['Hipotiroidismo', 'Obesidad', 'Anemia ferropénica'],
            'medicamentos': ['Levotiroxina 75mcg c/d', 'Sulfato ferroso 325mg c/d'],
            'alergias': 'Cefalosporinas',
            'última_consulta': datetime.now().isoformat()
        },
        'pac003': {
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'cedula': '11223344',
            'edad': 72,
            'genero': 'M',
            'email': 'carlos@example.com',
            'telefono': '555-9012',
            'diagnósticos': ['Insuficiencia renal crónica', 'Hipertensión', 'Diabetes Tipo 2', 'Cardiopatía'],
            'medicamentos': ['Lisinopril 10mg c/d', 'Nifedipino 30mg c/d', 'Atorvastatina 40mg c/d', 'Glibenclamida 5mg c/12h'],
            'alergias': 'Sulfonamidas',
            'última_consulta': datetime.now().isoformat()
        },
        'pac004': {
            'nombre': 'Ana',
            'apellido': 'Martínez',
            'cedula': '55667788',
            'edad': 35,
            'genero': 'F',
            'email': 'ana@example.com',
            'telefono': '555-3456',
            'diagnósticos': ['Hiperlipidemia'],
            'medicamentos': ['Pravastatina 20mg c/d'],
            'alergias': 'Ninguna conocida',
            'última_consulta': datetime.now().isoformat()
        },
        'pac005': {
            'nombre': 'Roberto',
            'apellido': 'Fernández',
            'cedula': '99887766',
            'edad': 58,
            'genero': 'M',
            'email': 'roberto@example.com',
            'telefono': '555-7890',
            'diagnósticos': ['Cirrosis hepática', 'Hipertensión portal', 'Síndrome hepatorenal'],
            'medicamentos': ['Espironolactona 50mg c/d', 'Furosemida 40mg c/d', 'Propranolol 40mg c/8h'],
            'alergias': 'Tetracicinas',
            'última_consulta': datetime.now().isoformat()
        }
    }
    
    # Guardar pacientes
    ia.pacientes = pacientes
    ia.guardar_bases_datos()
    
    print("[OK] Pacientes creados:")
    for pid, p in pacientes.items():
        print(f"  * {p['nombre']} {p['apellido']} ({p['cedula']}) - ID: {pid}")
    
    # Generar análisis de laboratorio iniciales
    print("\n[ANALISIS] Generando analisis de laboratorio...")
    
    # Análisis para Juan (diabetes descontrolada)
    ia.analizar_resultados_laboratorio('pac001', {
        'glucosa': 280,
        'hemoglobina': 9.2,
        'hematocrito': 27,
        'creatinina': 1.8,
        'presion_sistolica': 165,
        'presion_diastolica': 95,
        'colesterol_total': 280,
        'trigliceridos': 450,
        'hdl': 35,
        'ldl': 190,
        'ast': 38,
        'alt': 42,
        'sodio': 138,
        'potasio': 5.2,
        'bilirrubina': 0.8
    })
    print("  * Juan García: Glucosa 280, Creatinina 1.8, Presión 165/95")
    
    # Análisis para María (anemia)
    ia.analizar_resultados_laboratorio('pac002', {
        'glucosa': 88,
        'hemoglobina': 7.8,
        'hematocrito': 24,
        'creatinina': 0.9,
        'presion_sistolica': 128,
        'presion_diastolica': 78,
        'colesterol_total': 220,
        'trigliceridos': 180,
        'hdl': 45,
        'ldl': 145,
        'ast': 32,
        'alt': 29,
        'sodio': 140,
        'potasio': 4.2,
        'bilirrubina': 0.6
    })
    print("  * María López: Hemoglobina 7.8, Hematocrito 24")
    
    # Análisis para Carlos (IRC avanzada)
    ia.analizar_resultados_laboratorio('pac003', {
        'glucosa': 156,
        'hemoglobina': 9.5,
        'hematocrito': 29,
        'creatinina': 4.2,
        'presion_sistolica': 158,
        'presion_diastolica': 92,
        'colesterol_total': 195,
        'trigliceridos': 240,
        'hdl': 38,
        'ldl': 128,
        'ast': 35,
        'alt': 38,
        'sodio': 134,
        'potasio': 6.1,
        'bilirrubina': 1.1,
        'calcio': 7.8,
        'fosforo': 5.2
    })
    print("  * Carlos Rodríguez: Creatinina 4.2, Potasio 6.1 (CRITICO), Calcio 7.8")
    
    # Análisis para Ana (normal)
    ia.analizar_resultados_laboratorio('pac004', {
        'glucosa': 92,
        'hemoglobina': 13.5,
        'hematocrito': 40,
        'creatinina': 0.8,
        'presion_sistolica': 118,
        'presion_diastolica': 76,
        'colesterol_total': 215,
        'trigliceridos': 140,
        'hdl': 52,
        'ldl': 138,
        'ast': 28,
        'alt': 25,
        'sodio': 139,
        'potasio': 4.1,
        'bilirrubina': 0.5
    })
    print("  * Ana Martínez: Valores normales")
    
    # Análisis para Roberto (hepatopatía)
    ia.analizar_resultados_laboratorio('pac005', {
        'glucosa': 110,
        'hemoglobina': 8.5,
        'hematocrito': 26,
        'creatinina': 2.8,
        'presion_sistolica': 135,
        'presion_diastolica': 88,
        'colesterol_total': 140,
        'trigliceridos': 320,
        'hdl': 28,
        'ldl': 72,
        'bilirrubina': 3.2,
        'ast': 125,
        'alt': 95,
        'albumina': 2.8,
        'sodio': 130,
        'potasio': 5.8,
        'calcio': 8.2,
        'fosforo': 3.8
    })
    print("  * Roberto Fernández: Bilirrubina 3.2, AST 125, ALT 95 (Hepatopatía severa)")
    
    print("\n[LISTO] Setup completo. Pacientes listos para usar en annIA")

if __name__ == '__main__':
    crear_pacientes_realistas()
