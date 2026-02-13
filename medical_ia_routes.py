# medical_ia_routes.py - Rutas Flask para IA Médica Profesional

from flask import jsonify, request
from medical_ai import IAMedicaProfesional

ia_medica = IAMedicaProfesional()

def registrar_rutas_medicas(app):
    """Registra las rutas para IA Médica Profesional"""
    
    @app.route('/api/medical/buscar-paciente', methods=['POST'])
    def buscar_paciente():
        """
        Busca pacientes por diferentes criterios
        Body: {"criterio": "nombre", "valor": "Juan"}
        Criterios: id, nombre, cedula, apellido
        """
        try:
            datos = request.get_json()
            criterio = datos.get('criterio', 'nombre')
            valor = datos.get('valor', '')
            
            resultado = ia_medica.buscar_paciente(criterio, valor)
            
            return jsonify({
                'exito': True,
                'resultado': resultado
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/medical/perfil-paciente/<paciente_id>', methods=['GET'])
    def obtener_perfil(paciente_id):
        """Obtiene el perfil completo de un paciente"""
        try:
            perfil = ia_medica.obtener_perfil_paciente(paciente_id)
            
            return jsonify({
                'exito': True,
                'perfil': perfil
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/medical/analizar-laboratorio', methods=['POST'])
    def analizar_laboratorio():
        """
        Analiza resultados de laboratorio y detecta anomalías
        Body: {
            "paciente_id": "pac123",
            "resultados": {
                "glucosa": 180,
                "hemoglobina": 9.5,
                "creatinina": 2.1
            }
        }
        """
        try:
            datos = request.get_json()
            paciente_id = datos.get('paciente_id')
            resultados = datos.get('resultados', {})
            
            # Validar que hay paciente y resultados
            if not paciente_id:
                return jsonify({'error': 'paciente_id es requerido'}), 400
            if not resultados or len(resultados) == 0:
                return jsonify({'error': 'resultados no puede estar vacío'}), 400
            
            # Verificar que los valores son números
            for clave, valor in resultados.items():
                if valor is None or (isinstance(valor, str) and valor.strip() == ''):
                    return jsonify({'error': f'{clave} no puede estar vacío'}), 400
                try:
                    float(valor)
                except (ValueError, TypeError):
                    return jsonify({'error': f'{clave} debe ser un número válido, recibió: {valor}'}), 400
            
            análisis = ia_medica.analizar_resultados_laboratorio(paciente_id, resultados)
            
            return jsonify({
                'exito': True,
                'análisis': análisis
            })
        
        except Exception as e:
            import traceback
            print(f"Error en análisis: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': f'Error: {str(e)}'}), 400
    
    @app.route('/api/medical/alertas/<paciente_id>', methods=['GET'])
    def obtener_alertas(paciente_id):
        """Obtiene todas las alertas de un paciente"""
        try:
            solo_activas = request.args.get('solo_activas', 'true').lower() == 'true'
            alertas = ia_medica.obtener_alertas_paciente(paciente_id, solo_activas)
            
            return jsonify({
                'exito': True,
                'alertas': alertas
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/medical/generar-alerta', methods=['POST'])
    def generar_alerta():
        """
        Genera una alerta manual
        Body: {
            "paciente_id": "pac123",
            "tipo": "medicamento_contraindicado",
            "descripción": "Paciente alérgico a penicilina, se prescribió amoxicilina",
            "severidad": "CRÍTICO"
        }
        """
        try:
            datos = request.get_json()
            paciente_id = datos.get('paciente_id')
            tipo = datos.get('tipo')
            descripción = datos.get('descripción')
            severidad = datos.get('severidad', 'MODERADO')
            
            alerta = ia_medica.generar_alerta_manual(paciente_id, tipo, descripción, severidad)
            
            return jsonify({
                'exito': True,
                'alerta': alerta
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/medical/resumen-clínico/<paciente_id>', methods=['GET'])
    def resumen_clínico(paciente_id):
        """Genera un resumen clínico completo del paciente"""
        try:
            resumen = ia_medica.obtener_resumen_clínico(paciente_id)
            
            return jsonify({
                'exito': True,
                'resumen': resumen
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/medical/registrar-consulta', methods=['POST'])
    def registrar_consulta():
        """
        Registra una consulta médica
        Body: {
            "paciente_id": "pac123",
            "notas_médico": "Paciente con síntomas de...",
            "diagnóstico": "Hipertensión esencial",
            "recomendaciones": "Iniciar lisinopril..."
        }
        """
        try:
            datos = request.get_json()
            paciente_id = datos.get('paciente_id')
            notas = datos.get('notas_médico', '')
            diagnóstico = datos.get('diagnóstico', '')
            recomendaciones = datos.get('recomendaciones', '')
            
            consulta = ia_medica.registrar_consulta(
                paciente_id, notas, diagnóstico, recomendaciones
            )
            
            return jsonify({
                'exito': True,
                'consulta': consulta
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/medical/comparar-análisis/<paciente_id>', methods=['GET'])
    def comparar_análisis(paciente_id):
        """Compara últimos análisis del paciente para ver tendencias"""
        try:
            últimos_n = request.args.get('últimos', 5, type=int)
            tendencias = ia_medica.comparar_análisis_temporal(paciente_id, últimos_n)
            
            return jsonify({
                'exito': True,
                'tendencias': tendencias
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/medical/consultar-groq', methods=['POST'])
    def consultar_groq():
        """
        Consulta a Groq para análisis clínico
        Body: {
            "consulta": "Paciente con glucosa 280, qué hacer?",
            "contexto": "Paciente diabético tipo 2, edad 65"
        }
        """
        try:
            from web_ia import IAMedicaChat
            
            datos = request.get_json()
            consulta = datos.get('consulta', '')
            contexto = datos.get('contexto', '')
            
            if not consulta or not consulta.strip():
                return jsonify({'error': 'La consulta no puede estar vacía', 'exito': False}), 400
            
            chat = IAMedicaChat()
            respuesta = chat.consultar_médico(consulta, contexto)
            
            # Validar si hay error en la respuesta
            if 'error' in respuesta:
                print(f"[DEBUG] Error de Groq: {respuesta.get('error')}")
                return jsonify({
                    'exito': False,
                    'error': respuesta.get('error', 'Error al procesar la consulta')
                }), 400
            
            print(f"[DEBUG] Consulta exitosa: {consulta[:50]}...")
            
            return jsonify({
                'exito': True,
                'respuesta': respuesta
            })
        
        except Exception as e:
            print(f"[ERROR] Exception en consultar_groq: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return jsonify({
                'error': f'Error del servidor: {str(e)}'  , 
                'exito': False
            }), 400
    
    @app.route('/api/medical/estado', methods=['GET'])
    def estado_ia():
        """Verifica el estado de la IA médica profesional"""
        return jsonify({
            'estado': 'online',
            'tipo': 'IA Médica Profesional',
            'advertencia': 'Herramienta de apoyo clínico. No reemplaza responsabilidad médica.',
            'funciones': [
                'Búsqueda de pacientes',
                'Análisis de laboratorio',
                'Generación de alertas',
                'Comparación de tendencias',
                'Consulta con Groq',
                'Resumen clínico'
            ]
        })
