"""
Script de pruebas para validar el Sistema Medico Inteligente v2.0
Verifica que todos los componentes esten funcionando correctamente
"""

import json
import os
from datetime import datetime

def test_imports():
    """Verifica que todos los modulos se importan correctamente"""
    print("\n" + "="*50)
    print("TEST 1: Importacion de Modulos")
    print("="*50)
    
    try:
        from pacientes_db import GestorPacientes
        print("[OK] pacientes_db.py importado correctamente")
    except ImportError as e:
        print(f"[ERROR] Error importando pacientes_db: {e}")
        return False
    
    try:
        from medical_ai import AnalisisAIMedico
        print("[OK] medical_ai.py importado correctamente")
    except ImportError as e:
        print(f"[ERROR] Error importando medical_ai: {e}")
        return False
    
    try:
        from flask import Flask
        print("[OK] Flask importado correctamente")
    except ImportError as e:
        print(f"[ERROR] Error importando Flask: {e}")
        return False
    
    return True


def test_database():
    """Verifica que la base de datos funciona"""
    print("\n" + "="*50)
    print("TEST 2: Base de Datos")
    print("="*50)
    
    from pacientes_db import GestorPacientes
    
    # Crear gestor
    db = GestorPacientes()
    print("[OK] GestorPacientes instanciado")
    
    # Verificar archivo existe
    if os.path.exists("pacientes.json"):
        print("[OK] Archivo pacientes.json existe")
    else:
        print("[WARN] Archivo pacientes.json no existe (se creara)")
    
    # Agregar paciente de prueba
    paciente = db.agregar_paciente({
        'nombre': 'Test',
        'apellido': 'Paciente',
        'cedula': '9999999999',
        'edad': 45,
        'genero': 'M',
        'telefono': '5551234567',
        'email': 'test@example.com'
    })
    
    if paciente and "id" in paciente:
        print(f"[OK] Paciente de prueba creado: ID {paciente['id']}")
    else:
        print("[ERROR] Error creando paciente de prueba")
        return False
    
    # Obtener paciente
    obtenido = db.obtener_paciente(paciente['id'])
    if obtenido:
        print(f"[OK] Paciente recuperado: {obtenido['nombre']}")
    else:
        print("[ERROR] Error recuperando paciente")
        return False
    
    # Agregar diagnostico
    db.agregar_diagnostico(paciente['id'], "Diabetes Mellitus Tipo 2")
    print("[OK] Diagnostico agregado")
    
    # Agregar tratamiento
    db.agregar_tratamiento(
        paciente['id'],
        "Tratamiento Metformina",
        "Metformina",
        "500mg",
        "3 meses"
    )
    print("[OK] Tratamiento agregado")
    
    # Agregar estudio
    db.agregar_estudio(
        paciente['id'],
        "Laboratorio de sangre",
        "Glucosa 150 mg/dL"
    )
    print("[OK] Estudio agregado")
    
    # Verificar diagnosticos
    diags = db.obtener_diagnosticos(paciente['id'])
    if len(diags) > 0:
        print(f"[OK] Diagnosticos recuperados: {len(diags)}")
    else:
        print("[WARN] No hay diagnosticos recuperados")
    
    # Limpiar (eliminar paciente de prueba)
    db.eliminar_paciente(paciente['id'])
    print("[OK] Paciente de prueba eliminado (limpieza)")
    
    return True


def test_ai():
    """Verifica que el motor de IA funciona"""
    print("\n" + "="*50)
    print("TEST 3: Motor de Analisis IA")
    print("="*50)
    
    from medical_ai import AnalisisAIMedico
    from pacientes_db import GestorPacientes
    
    # Crear instancia IA
    ia = AnalisisAIMedico()
    print("[OK] AnalisisAIMedico instanciado")
    
    # Crear paciente de prueba
    db = GestorPacientes()
    paciente = db.agregar_paciente({
        'nombre': 'Prueba',
        'apellido': 'IA',
        'cedula': '1111111111',
        'edad': 65,
        'genero': 'M',
        'telefono': '5559999999',
        'email': 'ia@test.com',
        'peso': 95,
        'altura': 175
    })
    
    # Agregar diagnosticos criticos
    db.agregar_diagnostico(paciente['id'], "Infarto agudo de miocardio")
    db.agregar_diagnostico(paciente['id'], "Hipertension")
    db.agregar_diagnostico(paciente['id'], "Diabetes")
    
    # Obtener paciente completo
    paciente_completo = db.obtener_paciente(paciente['id'])
    
    # Analizar
    analisis = ia.analizar_paciente(paciente_completo)
    
    # Verificar resultados
    if "alertas" in analisis:
        print(f"[OK] Alertas detectadas: {len(analisis['alertas'])}")
        for alerta in analisis['alertas'][:2]:  # Mostrar primeras 2
            print(f"     - {alerta['mensaje']}")
    else:
        print("[WARN] No se detectaron alertas")
    
    if "patrones" in analisis:
        print(f"[OK] Patrones detectados: {len(analisis['patrones'])}")
    else:
        print("[WARN] No se detectaron patrones")
    
    if "score_riesgo" in analisis:
        print(f"[OK] Score de riesgo calculado: {analisis['score_riesgo']}/100")
    else:
        print("[WARN] Score de riesgo no calculado")
    
    if "recomendaciones" in analisis:
        print(f"[OK] Recomendaciones generadas: {len(analisis['recomendaciones'])}")
    else:
        print("[WARN] No se generaron recomendaciones")
    
    # Limpiar
    db.eliminar_paciente(paciente['id'])
    print("[OK] Paciente de prueba eliminado (limpieza)")
    
    return True


def test_templates():
    """Verifica que los archivos HTML existen"""
    print("\n" + "="*50)
    print("TEST 4: Archivos de Interfaz")
    print("="*50)
    
    templates_requeridos = [
        "templates/index.html",
        "templates/pacientes.html",
        "templates/medico_inteligente.html",
        "templates/home.html"
    ]
    
    for template in templates_requeridos:
        if os.path.exists(template):
            size = os.path.getsize(template)
            print(f"[OK] {template} ({size} bytes)")
        else:
            print(f"[ERROR] {template} NO ENCONTRADO")
            return False
    
    return True


def test_api_endpoints():
    """Verifica que la API esta correctamente configurada"""
    print("\n" + "="*50)
    print("TEST 5: Configuracion de API")
    print("="*50)
    
    try:
        from web_ia import app
        print("[OK] Aplicacion Flask cargada")
        
        # Listar rutas
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(rule.rule)
        
        print(f"[OK] Total de rutas registradas: {len(routes)}")
        
        # Rutas esperadas
        expected_routes = [
            '/medico-inteligente',
            '/pacientes',
            '/api/pacientes',
            '/api/analisis-paciente/<id_paciente>',
            '/api/alertas-paciente/<id_paciente>'
        ]
        
        for expected in expected_routes:
            if any(expected in route for route in routes):
                print(f"     [OK] {expected}")
            else:
                print(f"     [WARN] {expected} - Puede no estar disponible")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error verificando API: {e}")
        return False


def test_file_structure():
    """Verifica la estructura de archivos"""
    print("\n" + "="*50)
    print("TEST 6: Estructura de Archivos")
    print("="*50)
    
    required_files = {
        "Python": ["web_ia.py", "pacientes_db.py", "medical_ai.py"],
        "Templates": ["templates/medico_inteligente.html"],
        "Documentacion": ["GUIA_USUARIO_MEDICO.md", "CAPACIDADES_IA_DETALLADAS.md"]
    }
    
    all_ok = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  [OK] {file} ({size} bytes)")
            else:
                print(f"  [ERROR] {file} NO ENCONTRADO")
                all_ok = False
    
    return all_ok


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "SISTEMA MEDICO INTELIGENTE - PRUEBAS DE VALIDACION".center(52))
    print("=" * 52)
    print(f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Importacion de Modulos", test_imports),
        ("Base de Datos", test_database),
        ("Motor de IA", test_ai),
        ("Archivos de Interfaz", test_templates),
        ("Configuracion de API", test_api_endpoints),
        ("Estructura de Archivos", test_file_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[ERROR] Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "=" * 52)
    print("RESUMEN DE PRUEBAS")
    print("=" * 52)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASADO]" if result else "[FALLIDO]"
        print(f"{status} - {test_name}")
    
    print("=" * 52)
    print(f"RESULTADO: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n*** SISTEMA COMPLETAMENTE FUNCIONAL ***")
        print("\nPuedes iniciar el servidor con:")
        print("  python web_ia.py")
        print("\nY acceder a:")
        print("  http://localhost:5000/medico-inteligente")
    else:
        print(f"\n[ADVERTENCIA] {total - passed} prueba(s) fallida(s)")
        print("Revisa los errores arriba y la documentacion")
    
    print("=" * 52 + "\n")


if __name__ == "__main__":
    run_all_tests()
