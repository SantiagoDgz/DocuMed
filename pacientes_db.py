import json
import os
from datetime import datetime
from pathlib import Path

class GestorPacientes:
    """Gestor de base de datos de pacientes"""
    
    def __init__(self, archivo_db='pacientes.json'):
        self.archivo_db = archivo_db
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga los datos de pacientes desde el archivo JSON"""
        if os.path.exists(self.archivo_db):
            with open(self.archivo_db, 'r', encoding='utf-8') as f:
                self.pacientes = json.load(f)
        else:
            self.pacientes = {}
    
    def guardar_datos(self):
        """Guarda los datos de pacientes en el archivo JSON"""
        with open(self.archivo_db, 'w', encoding='utf-8') as f:
            json.dump(self.pacientes, f, ensure_ascii=False, indent=2)
    
    def agregar_paciente(self, datos_paciente):
        """Agrega un nuevo paciente"""
        # Generar ID único
        id_paciente = str(len(self.pacientes) + 1).zfill(5)
        
        paciente = {
            'id': id_paciente,
            'nombre': datos_paciente.get('nombre', ''),
            'apellido': datos_paciente.get('apellido', ''),
            'cedula': datos_paciente.get('cedula', ''),
            'edad': datos_paciente.get('edad', ''),
            'genero': datos_paciente.get('genero', ''),
            'telefono': datos_paciente.get('telefono', ''),
            'email': datos_paciente.get('email', ''),
            'direccion': datos_paciente.get('direccion', ''),
            'historia_medica': datos_paciente.get('historia_medica', ''),
            'alergias': datos_paciente.get('alergias', ''),
            'medicamentos': datos_paciente.get('medicamentos', ''),
            'peso': datos_paciente.get('peso', ''),
            'altura': datos_paciente.get('altura', ''),
            'presion_arterial': datos_paciente.get('presion_arterial', ''),
            'fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ultima_consulta': datos_paciente.get('ultima_consulta', ''),
            # NUEVOS CAMPOS CLÍNICOS AVANZADOS
            'diagnósticos': [],  # Lista de diagnósticos
            'tratamientos': [],  # Lista de tratamientos activos
            'estudios': [],  # Exámenes y estudios realizados
            'sintomas': datos_paciente.get('sintomas', ''),  # Síntomas actuales
            'observaciones': '',  # Observaciones clínicas
            'estado_clinico': 'Estable',  # Estado actual
            'riesgo_clinico': 'Bajo',  # Nivel de riesgo
            'notas': [],  # Historial de notas/consultas
            'timeline': []  # Timeline de eventos clínicos
        }
        
        self.pacientes[id_paciente] = paciente
        self.guardar_datos()
        return paciente
    
    def obtener_paciente(self, id_paciente):
        """Obtiene un paciente por ID"""
        return self.pacientes.get(id_paciente)
    
    def obtener_todos_pacientes(self):
        """Obtiene todos los pacientes"""
        return list(self.pacientes.values())
    
    def actualizar_paciente(self, id_paciente, datos_actualizacion):
        """Actualiza información de un paciente"""
        if id_paciente in self.pacientes:
            self.pacientes[id_paciente].update(datos_actualizacion)
            self.guardar_datos()
            return self.pacientes[id_paciente]
        return None
    
    def eliminar_paciente(self, id_paciente):
        """Elimina un paciente"""
        if id_paciente in self.pacientes:
            del self.pacientes[id_paciente]
            self.guardar_datos()
            return True
        return False
    
    def agregar_nota_paciente(self, id_paciente, nota):
        """Agrega una nota a la historia del paciente"""
        if id_paciente in self.pacientes:
            nota_obj = {
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'contenido': nota
            }
            self.pacientes[id_paciente]['notas'].append(nota_obj)
            self.guardar_datos()
            return nota_obj
        return None
    
    def buscar_paciente(self, termino):
        """Busca pacientes por nombre, apellido o cédula"""
        resultados = []
        termino = termino.lower()
        for paciente in self.pacientes.values():
            if (termino in paciente['nombre'].lower() or 
                termino in paciente['apellido'].lower() or 
                termino in paciente['cedula'].lower()):
                resultados.append(paciente)
        return resultados
    
    # MÉTODOS PARA DIAGNÓSTICOS
    def agregar_diagnostico(self, id_paciente, diagnostico, fecha=None):
        """Agrega un diagnóstico a un paciente"""
        if id_paciente in self.pacientes:
            if fecha is None:
                fecha = datetime.now().strftime('%Y-%m-%d')
            
            diag = {
                'diagnostico': diagnostico,
                'fecha': fecha,
                'activo': True
            }
            self.pacientes[id_paciente]['diagnósticos'].append(diag)
            self.guardar_datos()
            return diag
        return None
    
    def obtener_diagnosticos(self, id_paciente):
        """Obtiene todos los diagnósticos de un paciente"""
        if id_paciente in self.pacientes:
            return self.pacientes[id_paciente].get('diagnósticos', [])
        return []
    
    # MÉTODOS PARA TRATAMIENTOS
    def agregar_tratamiento(self, id_paciente, tratamiento, medicamento, dosis, duracion):
        """Agrega un tratamiento a un paciente"""
        if id_paciente in self.pacientes:
            tratamiento_obj = {
                'tratamiento': tratamiento,
                'medicamento': medicamento,
                'dosis': dosis,
                'duracion': duracion,
                'fecha_inicio': datetime.now().strftime('%Y-%m-%d'),
                'activo': True
            }
            self.pacientes[id_paciente]['tratamientos'].append(tratamiento_obj)
            self.guardar_datos()
            return tratamiento_obj
        return None
    
    def obtener_tratamientos(self, id_paciente):
        """Obtiene todos los tratamientos de un paciente"""
        if id_paciente in self.pacientes:
            return self.pacientes[id_paciente].get('tratamientos', [])
        return []
    
    # MÉTODOS PARA ESTUDIOS/EXÁMENES
    def agregar_estudio(self, id_paciente, tipo_estudio, resultado, fecha=None):
        """Agrega un estudio/examen a un paciente"""
        if id_paciente in self.pacientes:
            if fecha is None:
                fecha = datetime.now().strftime('%Y-%m-%d')
            
            estudio = {
                'tipo': tipo_estudio,
                'resultado': resultado,
                'fecha': fecha,
                'archivo': None
            }
            self.pacientes[id_paciente]['estudios'].append(estudio)
            self.guardar_datos()
            return estudio
        return None
    
    def obtener_estudios(self, id_paciente):
        """Obtiene todos los estudios de un paciente"""
        if id_paciente in self.pacientes:
            return self.pacientes[id_paciente].get('estudios', [])
        return []
    
    # MÉTODO PARA AGREGAR A TIMELINE
    def agregar_evento_timeline(self, id_paciente, tipo_evento, descripcion):
        """Agrega un evento al timeline clínico"""
        if id_paciente in self.pacientes:
            evento = {
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'tipo': tipo_evento,
                'descripcion': descripcion
            }
            self.pacientes[id_paciente]['timeline'].append(evento)
            self.guardar_datos()
            return evento
        return None
    
    def obtener_timeline(self, id_paciente):
        """Obtiene el timeline clínico de un paciente"""
        if id_paciente in self.pacientes:
            return sorted(
                self.pacientes[id_paciente].get('timeline', []),
                key=lambda x: x['fecha'],
                reverse=True
            )
        return []
    
    def actualizar_campo(self, id_paciente, campo, valor):
        """Actualiza un campo específico del paciente"""
        if id_paciente in self.pacientes:
            self.pacientes[id_paciente][campo] = valor
            self.guardar_datos()
            return True
        return False
    
    def agregar_nota(self, id_paciente, nota):
        """Agrega una nota al paciente"""
        return self.agregar_nota_paciente(id_paciente, nota)
