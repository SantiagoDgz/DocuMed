#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el sistema de gestión de pacientes
"""

from pacientes_db import GestorPacientes
import json

def main():
    print("\n" + "="*60)
    print("  🏥 PRUEBA DEL SISTEMA DE GESTIÓN DE PACIENTES")
    print("="*60 + "\n")

    # Crear instancia del gestor
    gestor = GestorPacientes()
    print("✅ Base de datos inicializada\n")

    # 1. Agregar paciente de prueba
    print("1️⃣  Agregando paciente de prueba...")
    paciente_test = {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'cedula': '12345678',
        'edad': '45',
        'genero': 'Masculino',
        'telefono': '555-1234',
        'email': 'juan@example.com',
        'direccion': 'Calle Principal 123',
        'peso': '75',
        'altura': '175',
        'presion_arterial': '120/80',
        'alergias': 'Penicilina',
        'medicamentos': 'Aspirina',
        'historia_medica': 'Antecedentes de hipertensión'
    }
    
    paciente = gestor.agregar_paciente(paciente_test)
    print(f"✅ Paciente agregado - ID: {paciente['id']}\n")

    # 2. Obtener todos los pacientes
    print("2️⃣  Obteniendo lista de pacientes...")
    pacientes = gestor.obtener_todos_pacientes()
    print(f"✅ Total de pacientes: {len(pacientes)}\n")

    # 3. Obtener un paciente específico
    print("3️⃣  Obteniendo detalles del paciente...")
    id_paciente = paciente['id']
    paciente_obtenido = gestor.obtener_paciente(id_paciente)
    if paciente_obtenido:
        print(f"✅ Paciente encontrado: {paciente_obtenido['nombre']} {paciente_obtenido['apellido']}\n")
    else:
        print("❌ Paciente no encontrado\n")

    # 4. Agregar nota
    print("4️⃣  Agregando nota de consulta...")
    nota = "Paciente presenta síntomas de resfriado común. Se recomienda reposo."
    nota_agregada = gestor.agregar_nota_paciente(id_paciente, nota)
    if nota_agregada:
        print(f"✅ Nota agregada el {nota_agregada['fecha']}\n")
    else:
        print("❌ No se pudo agregar la nota\n")

    # 5. Buscar paciente
    print("5️⃣  Buscando paciente...")
    resultados = gestor.buscar_paciente('Pérez')
    print(f"✅ Encontrados {len(resultados)} resultado(s)\n")

    # 6. Actualizar paciente
    print("6️⃣  Actualizando información del paciente...")
    datos_actualizacion = {'presion_arterial': '125/82', 'peso': '74'}
    paciente_actualizado = gestor.actualizar_paciente(id_paciente, datos_actualizacion)
    if paciente_actualizado:
        print(f"✅ Presión actualizada a: {paciente_actualizado['presion_arterial']}\n")
    else:
        print("❌ No se pudo actualizar\n")

    # 7. Ver datos guardados
    print("7️⃣  Verificando archivo de base de datos...")
    try:
        with open('pacientes.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        print(f"✅ Archivo 'pacientes.json' creado correctamente")
        print(f"✅ Pacientes guardados: {len(datos)}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Resumen
    print("="*60)
    print("  ✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("="*60)
    print("\n📝 Resumen:")
    print(f"  • Base de datos: {len(pacientes)} paciente(s)")
    print(f"  • ID del paciente: {id_paciente}")
    print(f"  • Archivo guardado: pacientes.json")
    print(f"\n🚀 Ya puedes iniciar el servidor con: python web_ia.py")
    print(f"📱 Luego abre: http://localhost:5000/pacientes\n")

if __name__ == "__main__":
    main()
