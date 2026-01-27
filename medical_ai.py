# medical_ai.py - Módulo de Inteligencia Artificial Médica

import json
from datetime import datetime, timedelta
from collections import defaultdict
import re

class AnalisisAIMedico:
    """Sistema de IA para análisis clínico y recomendaciones médicas"""
    
    def __init__(self):
        # Patrones de diagnósticos comunes
        self.diagnósticos_críticos = [
            'infarto', 'embolia', 'accidente cerebrovascular', 'sepsis',
            'cáncer', 'diabetes descontrolada', 'hipertensión severa'
        ]
        
        # Medicamentos incompatibles (ejemplo)
        self.incompatibilidades = {
            'warfarina': ['ibuprofeno', 'aspirina'],
            'metformina': ['alcohol'],
            'lisinopril': ['potasio'],
        }
    
    def analizar_paciente(self, paciente):
        """Análisis completo del paciente"""
        análisis = {
            'id': paciente.get('id'),
            'nombre': f"{paciente.get('nombre')} {paciente.get('apellido')}",
            'alertas': [],
            'recomendaciones': [],
            'patrones': [],
            'resumen_clinico': '',
            'score_riesgo': 0
        }
        
        # Análisis de alertas
        análisis['alertas'] = self._detectar_alertas(paciente)
        
        # Análisis de patrones
        análisis['patrones'] = self._detectar_patrones(paciente)
        
        # Recomendaciones
        análisis['recomendaciones'] = self._generar_recomendaciones(paciente)
        
        # Resumen clínico
        análisis['resumen_clinico'] = self._generar_resumen(paciente)
        
        # Score de riesgo (0-100)
        análisis['score_riesgo'] = self._calcular_riesgo(paciente)
        
        return análisis
    
    def _detectar_alertas(self, paciente):
        """Detecta alertas clínicas importantes"""
        alertas = []
        
        # Alerta de seguimiento vencido
        if paciente.get('ultima_consulta'):
            última = datetime.strptime(paciente['ultima_consulta'], '%Y-%m-%d')
            días_desde = (datetime.now() - última).days
            
            if días_desde > 180:
                alertas.append({
                    'tipo': 'seguimiento_vencido',
                    'nivel': 'alto',
                    'mensaje': f'Seguimiento vencido hace {días_desde} días',
                    'acción': 'Agendar cita de seguimiento urgente'
                })
            elif días_desde > 90:
                alertas.append({
                    'tipo': 'seguimiento_proximo',
                    'nivel': 'medio',
                    'mensaje': f'Última consulta hace {días_desde} días',
                    'acción': 'Considerar seguimiento próximamente'
                })
        
        # Alerta de presión arterial
        if paciente.get('presion_arterial'):
            try:
                sistólica, diastólica = map(int, paciente['presion_arterial'].split('/'))
                if sistólica >= 180 or diastólica >= 120:
                    alertas.append({
                        'tipo': 'hipertension_severa',
                        'nivel': 'crítico',
                        'mensaje': f'Presión arterial crítica: {paciente["presion_arterial"]}',
                        'acción': 'Evaluación médica inmediata recomendada'
                    })
                elif sistólica >= 140 or diastólica >= 90:
                    alertas.append({
                        'tipo': 'hipertension',
                        'nivel': 'alto',
                        'mensaje': f'Presión arterial elevada: {paciente["presion_arterial"]}',
                        'acción': 'Monitoreo recomendado'
                    })
            except:
                pass
        
        # Alerta de peso
        if paciente.get('peso') and paciente.get('altura'):
            try:
                peso = float(paciente['peso'])
                altura = float(paciente['altura']) / 100
                imc = peso / (altura ** 2)
                
                if imc > 35:
                    alertas.append({
                        'tipo': 'obesidad',
                        'nivel': 'alto',
                        'mensaje': f'IMC crítico: {imc:.1f}',
                        'acción': 'Intervención nutricional recomendada'
                    })
                elif imc > 30:
                    alertas.append({
                        'tipo': 'sobrepeso',
                        'nivel': 'medio',
                        'mensaje': f'Sobrepeso: IMC {imc:.1f}',
                        'acción': 'Plan de pérdida de peso recomendado'
                    })
            except:
                pass
        
        # Alerta de diagnósticos críticos
        if paciente.get('diagnósticos'):
            for diag in paciente['diagnósticos']:
                # Si es un diccionario, obtener la descripción
                diag_texto = diag.get('diagnostico', str(diag)) if isinstance(diag, dict) else diag
                diag_lower = diag_texto.lower()
                if any(crítico in diag_lower for crítico in self.diagnósticos_críticos):
                    alertas.append({
                        'tipo': 'diagnostico_critico',
                        'nivel': 'crítico',
                        'mensaje': f'Diagnóstico crítico detectado: {diag_texto}',
                        'acción': 'Seguimiento y evaluación periódica obligatoria'
                    })
        
        # Alerta de alergia a medicamento
        if paciente.get('alergias') and paciente.get('medicamentos'):
            alergias = paciente['alergias'].lower()
            meds = paciente['medicamentos'].lower()
            if 'penicilina' in alergias and 'amoxicilina' in meds:
                alertas.append({
                    'tipo': 'interaccion_peligrosa',
                    'nivel': 'crítico',
                    'mensaje': 'Posible reacción alérgica: Penicilina alérgico y con Amoxicilina',
                    'acción': 'REVISAR INMEDIATAMENTE'
                })
        
        return alertas
    
    def _detectar_patrones(self, paciente):
        """Detecta patrones en el historial"""
        patrones = []
        
        # Patrón: Múltiples diagnósticos relacionados
        if paciente.get('diagnósticos') and len(paciente['diagnósticos']) >= 2:
            patrones.append({
                'tipo': 'comorbilidad',
                'descripción': f'Paciente presenta {len(paciente["diagnósticos"])} diagnósticos',
                'implicación': 'Mayor riesgo de complicaciones'
            })
        
        # Patrón: Muchas notas recientes
        if paciente.get('notas'):
            notas_recientes = 0
            for nota in paciente['notas']:
                try:
                    fecha = datetime.strptime(nota.get('fecha', ''), '%Y-%m-%d %H:%M:%S')
                    if (datetime.now() - fecha).days <= 30:
                        notas_recientes += 1
                except:
                    pass
            
            if notas_recientes >= 4:
                patrones.append({
                    'tipo': 'consultoria_frecuente',
                    'descripción': f'{notas_recientes} consultas en último mes',
                    'implicación': 'Posible inestabilidad clínica'
                })
        
        return patrones
    
    def _generar_recomendaciones(self, paciente):
        """Genera recomendaciones personalizadas"""
        recomendaciones = []
        
        # Recomendación: Seguimiento
        if paciente.get('ultima_consulta'):
            última = datetime.strptime(paciente['ultima_consulta'], '%Y-%m-%d')
            días = (datetime.now() - última).days
            
            if días > 60:
                recomendaciones.append({
                    'prioridad': 'alta',
                    'tipo': 'seguimiento',
                    'texto': 'Agendar consulta de seguimiento',
                    'detalles': f'Última cita fue hace {días} días'
                })
        
        # Recomendación: Exámenes
        if paciente.get('edad'):
            try:
                edad = int(paciente['edad'])
                if edad >= 40:
                    recomendaciones.append({
                        'prioridad': 'media',
                        'tipo': 'examenes',
                        'texto': 'Evaluación cardiovascular recomendada',
                        'detalles': 'Por rango de edad (40+)'
                    })
                if edad >= 50:
                    recomendaciones.append({
                        'prioridad': 'media',
                        'tipo': 'examenes',
                        'texto': 'Screening de cáncer recomendado',
                        'detalles': 'Por rango de edad (50+)'
                    })
            except:
                pass
        
        # Recomendación: Estilo de vida
        if paciente.get('peso') and paciente.get('altura'):
            try:
                peso = float(paciente['peso'])
                altura = float(paciente['altura']) / 100
                imc = peso / (altura ** 2)
                
                if imc > 25:
                    recomendaciones.append({
                        'prioridad': 'media',
                        'tipo': 'estilo_vida',
                        'texto': 'Programa de pérdida de peso',
                        'detalles': 'Dieta balanceada + actividad física regular'
                    })
            except:
                pass
        
        return recomendaciones
    
    def _generar_resumen(self, paciente):
        """Genera resumen clínico inteligente"""
        resumen_partes = []
        
        # Demografía
        resumen_partes.append(
            f"Paciente: {paciente.get('nombre')} {paciente.get('apellido')}, "
            f"{paciente.get('edad')} años, {paciente.get('genero', 'No especificado')}"
        )
        
        # Diagnósticos
        if paciente.get('diagnósticos'):
            diags_list = []
            for diag in paciente['diagnósticos'][:3]:
                if isinstance(diag, dict):
                    diags_list.append(diag.get('diagnostico', str(diag)))
                else:
                    diags_list.append(str(diag))
            diags = ', '.join(diags_list)
            if len(paciente['diagnósticos']) > 3:
                diags += f" (+{len(paciente['diagnósticos'])-3} más)"
            resumen_partes.append(f"Diagnósticos: {diags}")
        
        # Medicamentos
        if paciente.get('medicamentos'):
            med_list = paciente['medicamentos'].split(',')[:3]
            meds = ', '.join([m.strip() for m in med_list])
            resumen_partes.append(f"Medicamentos: {meds}")
        
        # Alergias
        if paciente.get('alergias'):
            resumen_partes.append(f"⚠️ Alergias: {paciente['alergias']}")
        
        # Última consulta
        if paciente.get('ultima_consulta'):
            resumen_partes.append(f"Última consulta: {paciente['ultima_consulta']}")
        
        return " | ".join(resumen_partes)
    
    def _calcular_riesgo(self, paciente):
        """Calcula score de riesgo 0-100"""
        score = 0
        
        # Factores de riesgo
        if paciente.get('edad'):
            try:
                edad = int(paciente['edad'])
                if edad > 70:
                    score += 20
                elif edad > 50:
                    score += 10
            except:
                pass
        
        # Diagnósticos
        if paciente.get('diagnósticos'):
            score += min(len(paciente['diagnósticos']) * 10, 30)
        
        # Presión arterial
        if paciente.get('presion_arterial'):
            try:
                sistólica, diastólica = map(int, paciente['presion_arterial'].split('/'))
                if sistólica >= 180 or diastólica >= 120:
                    score += 20
                elif sistólica >= 140 or diastólica >= 90:
                    score += 10
            except:
                pass
        
        # IMC
        if paciente.get('peso') and paciente.get('altura'):
            try:
                peso = float(paciente['peso'])
                altura = float(paciente['altura']) / 100
                imc = peso / (altura ** 2)
                
                if imc > 35:
                    score += 15
                elif imc > 30:
                    score += 8
            except:
                pass
        
        # Tiempo sin consulta
        if paciente.get('ultima_consulta'):
            try:
                última = datetime.strptime(paciente['ultima_consulta'], '%Y-%m-%d')
                días = (datetime.now() - última).days
                if días > 180:
                    score += 10
            except:
                pass
        
        return min(score, 100)
    
    def resumir_historial(self, paciente):
        """Genera un resumen ejecutivo del historial"""
        return {
            'paciente_nombre': f"{paciente.get('nombre')} {paciente.get('apellido')}",
            'resumen_ejecutivo': self._generar_resumen(paciente),
            'diagnósticos_activos': paciente.get('diagnósticos', []),
            'medicamentos_activos': paciente.get('medicamentos', '').split(',') if paciente.get('medicamentos') else [],
            'alergias': paciente.get('alergias', 'Ninguna'),
            'estado_clinico': 'Estable' if paciente.get('presion_arterial') else 'Por confirmar',
            'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def detectar_inconsistencias(self, paciente):
        """Detecta datos faltantes o inconsistentes"""
        inconsistencias = []
        campos_obligatorios = ['nombre', 'apellido', 'cedula', 'edad']
        
        for campo in campos_obligatorios:
            if not paciente.get(campo):
                inconsistencias.append({
                    'tipo': 'faltante',
                    'campo': campo,
                    'mensaje': f'Campo obligatorio faltante: {campo}'
                })
        
        # Validar consistencia
        if paciente.get('peso') and paciente.get('altura'):
            try:
                peso = float(paciente['peso'])
                altura = float(paciente['altura'])
                
                if peso < 20 or peso > 200:
                    inconsistencias.append({
                        'tipo': 'inconsistencia',
                        'campo': 'peso',
                        'mensaje': f'Peso inusual: {peso} kg'
                    })
                
                if altura < 100 or altura > 250:
                    inconsistencias.append({
                        'tipo': 'inconsistencia',
                        'campo': 'altura',
                        'mensaje': f'Altura inusual: {altura} cm'
                    })
            except:
                pass
        
        # Validar presión arterial
        if paciente.get('presion_arterial'):
            if '/' not in paciente['presion_arterial']:
                inconsistencias.append({
                    'tipo': 'formato_incorrecto',
                    'campo': 'presion_arterial',
                    'mensaje': 'Formato debe ser: 120/80'
                })
        
        return inconsistencias
