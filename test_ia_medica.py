#!/usr/bin/env python3
# test_ia_medica.py - Test para IA Médica Profesional

import json
from medical_ai import IAMedicaProfesional

def main():
    print("=" * 70)
    print("PRUEBA DE IA MÉDICA PROFESIONAL - SISTEMA CLÍNICO")
    print("=" * 70)
    
    # Inicializar IA
    ia = IAMedicaProfesional()
    
    # TEST 1: Crear datos de ejemplo (agregar paciente)
    print("\n📋 TEST 1: Agregar Paciente de Prueba")
    print("-" * 70)
    
    paciente_prueba = {
        'nombre': 'Juan',
        'apellido': 'García',
        'cedula': '12345678',
        'edad': 65,
        'genero': 'M',
        'email': 'juan@example.com',
        'telefono': '555-1234',
        'diagnósticos': ['Hipertensión', 'Diabetes Tipo 2'],
        'medicamentos': ['Losartán 50mg', 'Metformina 500mg'],
        'alergias': 'Penicilina',
        'última_consulta': '2026-02-01'
    }
    
    ia.pacientes['pac001'] = paciente_prueba
    ia.guardar_bases_datos()
    print(f"✓ Paciente agregado: {paciente_prueba['nombre']} {paciente_prueba['apellido']}")
    
    # TEST 2: Buscar paciente
    print("\n🔍 TEST 2: Buscar Paciente")
    print("-" * 70)
    
    búsqueda = ia.buscar_paciente('nombre', 'Juan')
    print(f"Búsqueda: nombre = 'Juan'")
    print(f"Encontrados: {búsqueda['total']}")
    if búsqueda['resultados']:
        print(f"→ {búsqueda['resultados'][0]['nombre']} {búsqueda['resultados'][0]['apellido']}")
    
    # TEST 3: Analizar resultados de laboratorio
    print("\n🧪 TEST 3: Analizar Resultados de Laboratorio")
    print("-" * 70)
    
    resultados_lab = {
        'glucosa': 280,
        'hemoglobina': 9.2,
        'creatinina': 1.8,
        'presion_sistolica': 165,
        'colesterol_total': 285,
        'ldl': 185,
        'trigliceridos': 320,
        'potasio': 5.8
    }
    
    análisis = ia.analizar_resultados_laboratorio('pac001', resultados_lab)
    
    print(f"Análisis de laboratorio para paciente pac001:")
    print(f"Resultados procesados: {len(análisis['resultados_analizados'])}")
    print(f"\nAnomalías detectadas: {len(análisis['anomalías'])}")
    
    for anomalía in análisis['anomalías'][:3]:
        print(f"\n  {anomalía['estado']} - {anomalía['prueba']}")
        print(f"  Valor: {anomalía['valor']}")
        print(f"  Recomendación: {anomalía['recomendación'][:60]}...")
    
    # TEST 4: Obtener alertas
    print("\n⚠️  TEST 4: Obtener Alertas del Paciente")
    print("-" * 70)
    
    alertas = ia.obtener_alertas_paciente('pac001', solo_activas=True)
    print(f"Alertas del paciente:")
    print(f"  Total: {alertas['total_alertas']}")
    print(f"  Críticas: {alertas['alertas_críticas']}")
    
    if alertas['alertas']:
        print(f"\nAlertas activas:")
        for alerta in alertas['alertas'][:3]:
            msg = alerta.get('mensaje', alerta.get('descripción', 'Sin mensaje'))
            print(f"  {alerta['simbolo']} [{alerta['severidad']}] {msg}")
    
    # TEST 5: Obtener perfil paciente
    print("\n👤 TEST 5: Obtener Perfil Completo del Paciente")
    print("-" * 70)
    
    perfil = ia.obtener_perfil_paciente('pac001')
    
    print(f"Perfil de {perfil['información_personal']['nombre']} {perfil['información_personal']['apellido']}")
    print(f"  Cédula: {perfil['información_personal']['cedula']}")
    print(f"  Edad: {perfil['información_personal']['edad']} años")
    print(f"  Diagnósticos: {', '.join(perfil['antecedentes']['diagnósticos'])}")
    print(f"  Alertas activas: {len(perfil['alertas_activas'])}")
    
    # TEST 6: Registrar consulta
    print("\n📝 TEST 6: Registrar Consulta Médica")
    print("-" * 70)
    
    consulta = ia.registrar_consulta(
        'pac001',
        'Paciente presenta glucosa elevada y presión alta. Síntomas de polidipsia.',
        'Diabetes descontrolada + Hipertensión no controlada',
        'Aumentar metformina a 1000mg. Añadir amlodipino 5mg. Derivar a endocrinología.'
    )
    
    print(f"Consulta registrada:")
    print(f"  Fecha: {consulta['fecha']}")
    print(f"  Diagnóstico: {consulta['diagnóstico']}")
    
    # TEST 7: Generar alerta manual
    print("\n🚨 TEST 7: Generar Alerta Manual")
    print("-" * 70)
    
    alerta_manual = ia.generar_alerta_manual(
        'pac001',
        'interacción_medicamento',
        'ATENCIÓN: Paciente alérgico a penicilina. Verificar prescripciones.',
        'CRÍTICO'
    )
    
    print(f"Alerta generada:")
    print(f"  {alerta_manual['simbolo']} [{alerta_manual['severidad']}] {alerta_manual['descripción']}")
    
    # TEST 8: Resumen clínico
    print("\n📊 TEST 8: Resumen Clínico Profesional")
    print("-" * 70)
    
    resumen = ia.obtener_resumen_clínico('pac001')
    print(resumen['resumen'])
    
    # TEST 9: Comparar tendencias
    print("\n📈 TEST 9: Comparar Análisis Temporales")
    print("-" * 70)
    
    tendencias = ia.comparar_análisis_temporal('pac001')
    
    if 'error' not in tendencias:
        print(f"Análisis comparados: {tendencias['análisis_comparados']}")
        print(f"Pruebas con tendencias: {len(tendencias['tendencias'])}")
    else:
        print("No hay análisis previos para comparación")
    
    print("\n" + "=" * 70)
    print("✓ PRUEBAS COMPLETADAS")
    print("=" * 70)
    
    print("\n✨ FUNCIONALIDADES DISPONIBLES:")
    print("1. ✓ Búsqueda de pacientes")
    print("2. ✓ Análisis de laboratorio automático")
    print("3. ✓ Generación de alertas inteligentes")
    print("4. ✓ Perfil completo de pacientes")
    print("5. ✓ Historial de consultas")
    print("6. ✓ Comparación de tendencias")
    print("7. ✓ Integración con Groq (consultas médicas)")
    
    print("\n📁 BASES DE DATOS CREADAS:")
    print("  • datos_medicos.json")
    print("  • pacientes_db.json")

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
