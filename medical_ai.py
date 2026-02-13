# medical_ai.py - IA Médica Profesional para Ayuda Clínica

import json
from datetime import datetime
import os
import re

class IAMedicaProfesional:
    """IA Profesional para ayuda clínica: búsqueda de pacientes, análisis de datos y alertas"""
    
    def __init__(self):
        self.db_archivo = "datos_medicos.json"
        self.pacientes_archivo = "pacientes_db.json"  # BD de pacientes
        self.cargar_bases_datos()
        
        # Rangos normales de laboratorio (referencia profesional)
        self.rangos_normales = {
            'glucosa': {'min': 70, 'max': 100, 'unidad': 'mg/dL', 'nombre': 'Glucosa en ayunas'},
            'hemoglobina': {'min': 12, 'max': 17.5, 'unidad': 'g/dL', 'nombre': 'Hemoglobina'},
            'hematocrito': {'min': 36, 'max': 46, 'unidad': '%', 'nombre': 'Hematocrito'},
            'creatinina': {'min': 0.7, 'max': 1.3, 'unidad': 'mg/dL', 'nombre': 'Creatinina'},
            'presion_sistolica': {'min': 90, 'max': 120, 'unidad': 'mmHg', 'nombre': 'Presión Sistólica'},
            'presion_diastolica': {'min': 60, 'max': 80, 'unidad': 'mmHg', 'nombre': 'Presión Diastólica'},
            'colesterol_total': {'min': 0, 'max': 200, 'unidad': 'mg/dL', 'nombre': 'Colesterol Total'},
            'trigliceridos': {'min': 0, 'max': 150, 'unidad': 'mg/dL', 'nombre': 'Triglicéridos'},
            'hdl': {'min': 40, 'max': 1000, 'unidad': 'mg/dL', 'nombre': 'HDL (colesterol bueno)'},
            'ldl': {'min': 0, 'max': 100, 'unidad': 'mg/dL', 'nombre': 'LDL (colesterol malo)'},
            'bilirrubina': {'min': 0.2, 'max': 1.3, 'unidad': 'mg/dL', 'nombre': 'Bilirrubina'},
            'ast': {'min': 10, 'max': 40, 'unidad': 'U/L', 'nombre': 'AST'},
            'alt': {'min': 7, 'max': 56, 'unidad': 'U/L', 'nombre': 'ALT'},
            'albumina': {'min': 3.5, 'max': 5, 'unidad': 'g/dL', 'nombre': 'Albúmina'},
            'sodio': {'min': 136, 'max': 145, 'unidad': 'mEq/L', 'nombre': 'Sodio'},
            'potasio': {'min': 3.5, 'max': 5, 'unidad': 'mEq/L', 'nombre': 'Potasio'},
            'calcio': {'min': 8.5, 'max': 10.2, 'unidad': 'mg/dL', 'nombre': 'Calcio'},
            'fosforo': {'min': 2.5, 'max': 4.5, 'unidad': 'mg/dL', 'nombre': 'Fósforo'},
        }
        
        # Criterios de alerta clínico
        self.criterios_alerta = {
            'CRÍTICO': {'color': '#FF0000', 'simbolo': '🔴', 'accion': 'Intervención inmediata'},
            'ALTO': {'color': '#FF6600', 'simbolo': '🟠', 'accion': 'Revisión urgente'},
            'MODERADO': {'color': '#FFCC00', 'simbolo': '🟡', 'accion': 'Monitoreo'},
            'NORMAL': {'color': '#00CC00', 'simbolo': '🟢', 'accion': 'Monitoreo rutinario'},
        }
    
    def cargar_bases_datos(self):
        """Carga las bases de datos"""
        # BD Médica
        if os.path.exists(self.db_archivo):
            try:
                with open(self.db_archivo, 'r', encoding='utf-8') as f:
                    datos_cargados = json.load(f)
                    # Validar estructura
                    if 'alertas' not in datos_cargados:
                        datos_cargados['alertas'] = []
                    if 'historial_analisis' not in datos_cargados:
                        datos_cargados['historial_analisis'] = []
                    if 'consultas' not in datos_cargados:
                        datos_cargados['consultas'] = []
                    self.datos = datos_cargados
            except:
                self.datos = {
                    'consultas': [],
                    'historial_analisis': [],
                    'alertas': []
                }
        else:
            self.datos = {
                'consultas': [],
                'historial_analisis': [],
                'alertas': []
            }
        
        # BD Pacientes
        if os.path.exists(self.pacientes_archivo):
            try:
                with open(self.pacientes_archivo, 'r', encoding='utf-8') as f:
                    self.pacientes = json.load(f)
            except:
                self.pacientes = {}
        else:
            self.pacientes = {}
    
    def guardar_bases_datos(self):
        """Guarda las bases de datos"""
        with open(self.db_archivo, 'w', encoding='utf-8') as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)
        
        with open(self.pacientes_archivo, 'w', encoding='utf-8') as f:
            json.dump(self.pacientes, f, indent=2, ensure_ascii=False)
    
    def buscar_paciente(self, criterio, valor):
        """
        Busca pacientes por ID, nombre, cédula, etc.
        criterio: 'id', 'nombre', 'cedula', 'email'
        """
        resultados = []
        
        for pid, paciente in self.pacientes.items():
            if criterio == 'id' and pid == valor:
                resultados.append({**paciente, 'id': pid})
            elif criterio == 'nombre' and valor.lower() in paciente.get('nombre', '').lower():
                resultados.append({**paciente, 'id': pid})
            elif criterio == 'cedula' and paciente.get('cedula') == valor:
                resultados.append({**paciente, 'id': pid})
            elif criterio == 'apellido' and valor.lower() in paciente.get('apellido', '').lower():
                resultados.append({**paciente, 'id': pid})
        
        return {
            'total': len(resultados),
            'resultados': resultados,
            'fecha_busqueda': datetime.now().isoformat()
        }
    
    def obtener_perfil_paciente(self, paciente_id):
        """Obtiene el perfil completo de un paciente"""
        if paciente_id not in self.pacientes:
            return {'error': 'Paciente no encontrado'}
        
        paciente = self.pacientes[paciente_id]
        
        # Obtener historial de análisis
        historial_analisis = [a for a in self.datos['historial_analisis'] if a['paciente_id'] == paciente_id]
        
        # Obtener alertas activas
        alertas_activas = [a for a in self.datos['alertas'] if a['paciente_id'] == paciente_id and a['estado'] == 'activa']
        
        return {
            'paciente_id': paciente_id,
            'información_personal': {
                'nombre': paciente.get('nombre'),
                'apellido': paciente.get('apellido'),
                'cedula': paciente.get('cedula'),
                'edad': paciente.get('edad'),
                'género': paciente.get('genero'),
                'email': paciente.get('email'),
                'teléfono': paciente.get('telefono')
            },
            'antecedentes': {
                'diagnósticos': paciente.get('diagnósticos', []),
                'medicamentos': paciente.get('medicamentos', []),
                'alergias': paciente.get('alergias', []),
                'cirugías': paciente.get('cirugías', [])
            },
            'vitales_últimos': paciente.get('vitales_últimos', {}),
            'último_análisis': historial_analisis[-1] if historial_analisis else None,
            'alertas_activas': alertas_activas,
            'última_visita': paciente.get('última_consulta')
        }
    
    def analizar_resultados_laboratorio(self, paciente_id, resultados):
        """
        Analiza resultados de laboratorio y detecta anomalías
        resultados: {'glucosa': 180, 'hemoglobina': 9.5, ...}
        """
        análisis = {
            'paciente_id': paciente_id,
            'fecha': datetime.now().isoformat(),
            'resultados_analizados': [],
            'anomalías': [],
            'alertas_generadas': []
        }
        
        for prueba, valor in resultados.items():
            prueba_lower = prueba.lower()
            
            if prueba_lower in self.rangos_normales:
                rango = self.rangos_normales[prueba_lower]
                estado = 'NORMAL'
                
                if valor < rango['min']:
                    estado = 'BAJO'
                    if prueba_lower in ['glucosa', 'hemoglobina', 'potasio']:
                        estado = 'CRÍTICO' if valor < rango['min'] * 0.7 else 'ALTO'
                elif valor > rango['max']:
                    estado = 'ALTO'
                    if prueba_lower in ['glucosa', 'creatinina', 'colesterol_total']:
                        estado = 'CRÍTICO' if valor > rango['max'] * 1.5 else 'MODERADO'
                
                resultado = {
                    'prueba': rango['nombre'],
                    'valor': valor,
                    'unidad': rango['unidad'],
                    'rango_normal': f"{rango['min']} - {rango['max']}",
                    'estado': estado,
                    'desviación': f"{((valor - rango['min']) / (rango['max'] - rango['min']) * 100):.1f}%"
                }
                
                análisis['resultados_analizados'].append(resultado)
                
                # Detectar anomalías
                if estado != 'NORMAL':
                    análisis['anomalías'].append({
                        'prueba': rango['nombre'],
                        'valor': valor,
                        'estado': estado,
                        'recomendación': self._generar_recomendacion(prueba_lower, valor, rango)
                    })
                    
                    # Generar alerta si es crítico
                    if estado == 'CRÍTICO':
                        alerta = self._generar_alerta(paciente_id, prueba_lower, valor, rango)
                        análisis['alertas_generadas'].append(alerta)
        
        # Guardar análisis
        self.datos['historial_analisis'].append(análisis)
        self.guardar_bases_datos()
        
        return análisis
    
    def _generar_recomendacion(self, prueba, valor, rango):
        """Genera recomendación clínica basada en resultado"""
        recomendaciones = {
            'glucosa': 'Evaluar diabetes. Considerar HbA1c. Derivar a endocrinología si está elevada persistentemente.',
            'hemoglobina': 'Evaluar anemia. Solicitar hierro, B12, ácido fólico. Investigar causa de la anemia.',
            'creatinina': 'Evaluar función renal. Calcular TFG. Monitorear presión arterial.',
            'presion_sistolica': 'Monitorear presión. Considerar antihipertensivos si está elevada.',
            'colesterol_total': 'Evaluar perfil lipídico completo. Considerar estatinas.',
            'ast': 'Evaluar función hepática. Solicitar ecografía hepática si está muy elevada.',
            'alt': 'Evaluar función hepática. Investigar posible hepatitis o esteatosis.',
            'potasio': 'Monitorear electrocardiograma. Evaluar medicamentos que afecten potasio.',
            'sodio': 'Evaluar balance de fluidos. Investigar posible deshidratación o SIADH.'
        }
        
        return recomendaciones.get(prueba, 'Revisar con especialista si es necesario')
    
    def _generar_alerta(self, paciente_id, prueba, valor, rango):
        """Genera una alerta clínica crítica"""
        alerta = {
            'paciente_id': paciente_id,
            'fecha': datetime.now().isoformat(),
            'tipo': 'resultado_crítico',
            'prueba': rango['nombre'],
            'valor': valor,
            'severidad': 'CRÍTICO',
            'simbolo': '🔴',
            'mensaje': f"{rango['nombre']}: {valor} {rango['unidad']} (rango normal: {rango['min']}-{rango['max']})",
            'accion': 'Requiere revisión e intervención inmediata',
            'estado': 'activa'
        }
        
        # Guardar alerta
        self.datos['alertas'].append(alerta)
        self.guardar_bases_datos()
        
        return alerta
    
    def obtener_alertas_paciente(self, paciente_id, solo_activas=False):
        """Obtiene alertas de un paciente"""
        alertas = self.datos['alertas']
        
        if solo_activas:
            alertas = [a for a in alertas if a['paciente_id'] == paciente_id and a['estado'] == 'activa']
        else:
            alertas = [a for a in alertas if a['paciente_id'] == paciente_id]
        
        return {
            'paciente_id': paciente_id,
            'total_alertas': len(alertas),
            'alertas_críticas': len([a for a in alertas if a['severidad'] == 'CRÍTICO' and a['estado'] == 'activa']),
            'alertas': alertas
        }
    
    def generar_alerta_manual(self, paciente_id, tipo, descripción, severidad='MODERADO'):
        """Genera una alerta manual por el médico"""
        alerta = {
            'paciente_id': paciente_id,
            'fecha': datetime.now().isoformat(),
            'tipo': tipo,
            'descripción': descripción,
            'severidad': severidad,
            'simbolo': self.criterios_alerta[severidad]['simbolo'],
            'estado': 'activa',
            'creada_por': 'médico'
        }
        
        self.datos['alertas'].append(alerta)
        self.guardar_bases_datos()
        
        return alerta
    
    def cerrar_alerta(self, alerta_id, notas=''):
        """Cierra una alerta (la marca como resuelta)"""
        for alerta in self.datos['alertas']:
            if alerta.get('id') == alerta_id or alerta == alerta_id:
                alerta['estado'] = 'resuelta'
                alerta['fecha_resolución'] = datetime.now().isoformat()
                alerta['notas'] = notas
                break
        
        self.guardar_bases_datos()
    
    def obtener_resumen_clínico(self, paciente_id):
        """Genera un resumen clínico profesional del paciente"""
        paciente = self.pacientes.get(paciente_id)
        if not paciente:
            return {'error': 'Paciente no encontrado'}
        
        historial_analisis = [a for a in self.datos['historial_analisis'] if a['paciente_id'] == paciente_id]
        alertas_activas = [a for a in self.datos['alertas'] if a['paciente_id'] == paciente_id and a['estado'] == 'activa']
        
        resumen = f"""
╔════════════════════════════════════════════════════════════╗
║           RESUMEN CLÍNICO DEL PACIENTE
╚════════════════════════════════════════════════════════════╝

📋 INFORMACIÓN PERSONAL
─────────────────────────
• Nombre: {paciente.get('nombre')} {paciente.get('apellido')}
• Cédula: {paciente.get('cedula')}
• Edad: {paciente.get('edad')} años
• Género: {paciente.get('genero')}
• Contacto: {paciente.get('email')} | {paciente.get('telefono')}

🏥 ANTECEDENTES MÉDICOS
─────────────────────────
• Diagnósticos: {', '.join(paciente.get('diagnósticos', [])) or 'Ninguno'}
• Medicamentos: {', '.join(paciente.get('medicamentos', [])) or 'Ninguno'}
• Alergias: {paciente.get('alergias') or 'Ninguna'}
• Cirugías previas: {', '.join(paciente.get('cirugías', [])) or 'Ninguna'}

⚠️ ALERTAS ACTIVAS: {len(alertas_activas)}
─────────────────────────"""
        
        for alerta in alertas_activas[:5]:
            resumen += f"\n{alerta['simbolo']} [{alerta['severidad']}] {alerta.get('prueba', alerta.get('tipo'))}"
        
        resumen += f"\n\n📊 ANÁLISIS RECIENTES: {len(historial_analisis)}"
        if historial_analisis:
            último = historial_analisis[-1]
            resumen += f"\n└─ Última fecha: {último['fecha']}"
        
        resumen += "\n\n" + "═" * 60
        
        return {'resumen': resumen, 'paciente_id': paciente_id}
    
    def registrar_consulta(self, paciente_id, notas_médico, diagnóstico='', recomendaciones=''):
        """Registra una consulta médica"""
        consulta = {
            'paciente_id': paciente_id,
            'fecha': datetime.now().isoformat(),
            'notas': notas_médico,
            'diagnóstico': diagnóstico,
            'recomendaciones': recomendaciones
        }
        
        self.datos['consultas'].append(consulta)
        
        # Actualizar última consulta del paciente
        if paciente_id in self.pacientes:
            self.pacientes[paciente_id]['última_consulta'] = datetime.now().isoformat()
        
        self.guardar_bases_datos()
        
        return consulta
    
    def comparar_análisis_temporal(self, paciente_id, últimos_n=5):
        """Compara últimos análisis del paciente para ver tendencias"""
        historial = [a for a in self.datos['historial_analisis'] if a['paciente_id'] == paciente_id][-últimos_n:]
        
        if not historial:
            return {'error': 'No hay análisis previos'}
        
        # Extraer pruebas comunes y crear tendencias
        tendencias = {}
        
        for análisis in historial:
            for resultado in análisis.get('resultados_analizados', []):
                prueba = resultado['prueba']
                if prueba not in tendencias:
                    tendencias[prueba] = []
                
                tendencias[prueba].append({
                    'fecha': análisis['fecha'],
                    'valor': resultado['valor'],
                    'estado': resultado['estado']
                })
        
        return {
            'paciente_id': paciente_id,
            'análisis_comparados': len(historial),
            'tendencias': tendencias,
            'fecha_generación': datetime.now().isoformat()
        }
