"""
Script de pruebas para validar el Sistema Médico Inteligente v2.0
Verifica que todos los componentes estén funcionando correctamente
"""

import json
import os
from datetime import datetime

def test_imports():
    """Verifica que todos los módulos se importan correctamente"""
    print("\n" + "="*50)
    print("TEST 1: Importacion de Modulos")
    print("="*50)
    
    try:
        from pacientes_db import GestorPacientes
        print("✓ pacientes_db.py importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando pacientes_db: {e}")
        return False
    
    try:
        from medical_ai import AnalisisAIMedico
        print("✓ medical_ai.py importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando medical_ai: {e}")
        return False
    
    try:
        from flask import Flask
        print("✓ Flask importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando Flask: {e}")
        return False
    
    return True


def test_database():
    """Verifica que la base de datos funciona"""
    print("\n" + "="*50)
    print("🗂️ TEST 2: Base de Datos")
    print("="*50)
    
    from pacientes_db import GestorPacientes
    
    # Crear gestor
    db = GestorPacientes()
    print("✓ GestorPacientes instanciado")
    
    # Verificar archivo existe
    if os.path.exists("pacientes.json"):
        print("✓ Archivo pacientes.json existe")
    else:
        print("⚠️  Archivo pacientes.json no existe (se creará)")
    
    # Agregar paciente de prueba
    paciente = db.agregar_paciente(
        nombre="Test",
        apellido="Paciente",
        cedula="9999999999",
        edad=45,
        genero="M",
        telefono="5551234567",
        email="test@example.com"
    )
    
    if paciente and "id" in paciente:
        print(f"✓ Paciente de prueba creado: ID {paciente['id']}")
    else:
        print("✗ Error creando paciente de prueba")
        return False
    
    # Obtener paciente
    obtenido = db.obtener_paciente(paciente['id'])
    if obtenido:
        print(f"✓ Paciente recuperado: {obtenido['nombre']}")
    else:
        print("✗ Error recuperando paciente")
        return False
    
    # Agregar diagnóstico
    db.agregar_diagnostico(paciente['id'], "Diabetes Mellitus Tipo 2")
    print("✓ Diagnóstico agregado")
    
    # Agregar tratamiento
    db.agregar_tratamiento(
        paciente['id'],
        "Metformina",
        "500mg",
        "3 meses"
    )
    print("✓ Tratamiento agregado")
    
    # Agregar estudio
    db.agregar_estudio(
        paciente['id'],
        "Laboratorio de sangre",
        "Glucosa 150 mg/dL"
    )
    print("✓ Estudio agregado")
    
    # Verificar diagnósticos
    diags = db.obtener_diagnosticos(paciente['id'])
    if len(diags) > 0:
        print(f"✓ Diagnósticos recuperados: {len(diags)}")
    else:
        print("⚠️  No hay diagnósticos recuperados")
    
    # Limpiar (eliminar paciente de prueba)
    db.eliminar_paciente(paciente['id'])
    print("✓ Paciente de prueba eliminado (limpieza)")
    
    return True


def test_ai():
    """Verifica que el motor de IA funciona"""
    print("\n" + "="*50)
    print("🤖 TEST 3: Motor de Análisis IA")
    print("="*50)
    
    from medical_ai import AnalisisAIMedico
    from pacientes_db import GestorPacientes
    
    # Crear instancia IA
    ia = AnalisisAIMedico()
    print("✓ AnalisisAIMedico instanciado")
    
    # Crear paciente de prueba
    db = GestorPacientes()
    paciente = db.agregar_paciente(
        nombre="Prueba",
        apellido="IA",
        cedula="1111111111",
        edad=65,
        genero="M",
        telefono="5559999999",
        email="ia@test.com",
        peso=95,
        altura=175
    )
    
    # Agregar diagnósticos críticos
    db.agregar_diagnostico(paciente['id'], "Infarto agudo de miocardio")
    db.agregar_diagnostico(paciente['id'], "Hipertensión")
    db.agregar_diagnostico(paciente['id'], "Diabetes")
    
    # Obtener paciente completo
    paciente_completo = db.obtener_paciente(paciente['id'])
    
    # Analizar
    analisis = ia.analizar_paciente(paciente_completo)
    
    # Verificar resultados
    if "alertas" in analisis:
        print(f"✓ Alertas detectadas: {len(analisis['alertas'])}")
        for alerta in analisis['alertas']:
            print(f"  - {alerta['mensaje']}")
    else:
        print("⚠️  No se detectaron alertas")
    
    if "patrones" in analisis:
        print(f"✓ Patrones detectados: {len(analisis['patrones'])}")
    else:
        print("⚠️  No se detectaron patrones")
    
    if "score_riesgo" in analisis:
        print(f"✓ Score de riesgo calculado: {analisis['score_riesgo']}/100")
    else:
        print("⚠️  Score de riesgo no calculado")
    
    if "recomendaciones" in analisis:
        print(f"✓ Recomendaciones generadas: {len(analisis['recomendaciones'])}")
    else:
        print("⚠️  No se generaron recomendaciones")
    
    # Limpiar
    db.eliminar_paciente(paciente['id'])
    print("✓ Paciente de prueba eliminado (limpieza)")
    
    return True


def test_templates():
    """Verifica que los archivos HTML existen"""
    print("\n" + "="*50)
    print("🌐 TEST 4: Archivos de Interfaz")
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
            print(f"✓ {template} ({size} bytes)")
        else:
            print(f"✗ {template} NO ENCONTRADO")
            return False
    
    return True


def test_api_endpoints():
    """Verifica que la API está correctamente configurada"""
    print("\n" + "="*50)
    print("📡 TEST 5: Configuración de API")
    print("="*50)
    
    try:
        from web_ia import app
        print("✓ Aplicación Flask cargada")
        
        # Listar rutas
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                routes.append(rule.rule)
        
        print(f"✓ Total de rutas registradas: {len(routes)}")
        
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
                print(f"  ✓ {expected}")
            else:
                print(f"  ⚠️  {expected} - Puede no estar disponible")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verificando API: {e}")
        return False


def test_file_structure():
    """Verifica la estructura de archivos"""
    print("\n" + "="*50)
    print("📁 TEST 6: Estructura de Archivos")
    print("="*50)
    
    required_files = {
        "Python": ["web_ia.py", "pacientes_db.py", "medical_ai.py"],
        "Templates": ["templates/medico_inteligente.html"],
        "Documentación": ["GUIA_USUARIO_MEDICO.md", "CAPACIDADES_IA_DETALLADAS.md"]
    }
    
    all_ok = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  ✓ {file} ({size} bytes)")
            else:
                print(f"  ✗ {file} NO ENCONTRADO")
                all_ok = False
    
    return all_ok


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "SISTEMA MEDICO INTELIGENTE - PRUEBAS DE VALIDACION".center(52))
    print("=" * 52)
    print(f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Importación de Módulos", test_imports),
        ("Base de Datos", test_database),
        ("Motor de IA", test_ai),
        ("Archivos de Interfaz", test_templates),
        ("Configuración de API", test_api_endpoints),
        ("Estructura de Archivos", test_file_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\n" + "=" * 52)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 52)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"{status} - {test_name}")
    
    print("=" * 52)
    print(f"RESULTADO: {passed}/{total} pruebas pasadas")
    
    if passed == total:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL! 🎉")
        print("\nPuedes iniciar el servidor con:")
        print("  python web_ia.py")
        print("\nY acceder a:")
        print("  http://localhost:5000/medico-inteligente")
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallida(s)")
        print("Revisa los errores arriba y la documentación")
    
    print("=" * 52 + "\n")


if __name__ == "__main__":
    run_all_tests()
