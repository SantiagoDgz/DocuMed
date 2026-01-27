"""
Módulo de sincronización con la nube
Realiza backup y sincronización de datos del sistema médico
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path


class SincronizadorNube:
    """Gestor de sincronización de datos con servicios en la nube"""
    
    def __init__(self, directorio_local='./datos_backup', archivo_config='config_nube.json'):
        """
        Inicializa el sincronizador
        
        Args:
            directorio_local: Directorio local para backups
            archivo_config: Archivo de configuración de nube
        """
        self.directorio_local = directorio_local
        self.archivo_config = archivo_config
        self.historial_sincronizacion = []
        self.configuracion = {}
        
        # Crear directorio de backup si no existe
        Path(self.directorio_local).mkdir(parents=True, exist_ok=True)
        self.cargar_configuracion()
        self.cargar_historial()
    
    def cargar_configuracion(self):
        """Carga configuración de servicios en la nube"""
        try:
            if os.path.exists(self.archivo_config):
                with open(self.archivo_config, 'r') as f:
                    self.configuracion = json.load(f)
            else:
                # Configuración por defecto (simulada)
                self.configuracion = {
                    'dropbox': {
                        'habilitado': False,
                        'token': '',
                        'carpeta': '/Medico_Sistema'
                    },
                    'google_drive': {
                        'habilitado': False,
                        'api_key': '',
                        'carpeta_id': ''
                    },
                    'aws_s3': {
                        'habilitado': False,
                        'access_key': '',
                        'secret_key': '',
                        'bucket': 'medico-backup'
                    },
                    'local': {
                        'habilitado': True,
                        'ruta': self.directorio_local
                    }
                }
                self.guardar_configuracion()
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
    
    def guardar_configuracion(self):
        """Guarda configuración de servicios en la nube"""
        try:
            with open(self.archivo_config, 'w') as f:
                json.dump(self.configuracion, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def crear_backup_completo(self, archivos_a_respaldar):
        """
        Crea backup completo de los datos
        
        Args:
            archivos_a_respaldar: Lista de archivos a respaldar
        
        Returns:
            dict con información del backup
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_backup = f'backup_{timestamp}'
            ruta_backup = os.path.join(self.directorio_local, nombre_backup)
            
            # Crear directorio de backup
            os.makedirs(ruta_backup, exist_ok=True)
            
            archivos_copiados = []
            tamaño_total = 0
            
            for archivo in archivos_a_respaldar:
                if os.path.exists(archivo):
                    nombre_archivo = os.path.basename(archivo)
                    ruta_destino = os.path.join(ruta_backup, nombre_archivo)
                    
                    shutil.copy2(archivo, ruta_destino)
                    tamaño_archivo = os.path.getsize(ruta_destino)
                    
                    archivos_copiados.append({
                        'archivo': nombre_archivo,
                        'tamaño': tamaño_archivo,
                        'estado': 'éxito'
                    })
                    
                    tamaño_total += tamaño_archivo
            
            # Crear metadatos del backup
            metadatos = {
                'nombre': nombre_backup,
                'timestamp': datetime.now().isoformat(),
                'archivos': archivos_copiados,
                'tamaño_total': tamaño_total,
                'tipo': 'completo',
                'estado': 'completado'
            }
            
            # Guardar metadatos
            with open(os.path.join(ruta_backup, 'metadata.json'), 'w') as f:
                json.dump(metadatos, f, indent=2, ensure_ascii=False)
            
            self.historial_sincronizacion.append(metadatos)
            self.guardar_historial()
            
            return metadatos
            
        except Exception as e:
            print(f"Error al crear backup: {e}")
            return None
    
    def crear_backup_incremental(self, archivos_a_respaldar, ultimo_backup):
        """
        Crea backup incremental (solo cambios desde último backup)
        
        Args:
            archivos_a_respaldar: Lista de archivos a respaldar
            ultimo_backup: Ruta del último backup
        
        Returns:
            dict con información del backup incremental
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_backup = f'backup_incremental_{timestamp}'
            ruta_backup = os.path.join(self.directorio_local, nombre_backup)
            
            os.makedirs(ruta_backup, exist_ok=True)
            
            archivos_copiados = []
            tamaño_total = 0
            
            for archivo in archivos_a_respaldar:
                if os.path.exists(archivo):
                    # Comparar timestamp
                    tiempo_archivo = os.path.getmtime(archivo)
                    nombre_archivo = os.path.basename(archivo)
                    ruta_destino = os.path.join(ruta_backup, nombre_archivo)
                    
                    # Si es más nuevo que el último backup, copiar
                    if tiempo_archivo > os.path.getmtime(ultimo_backup):
                        shutil.copy2(archivo, ruta_destino)
                        tamaño_archivo = os.path.getsize(ruta_destino)
                        
                        archivos_copiados.append({
                            'archivo': nombre_archivo,
                            'tamaño': tamaño_archivo,
                            'estado': 'nuevo'
                        })
                        
                        tamaño_total += tamaño_archivo
            
            metadatos = {
                'nombre': nombre_backup,
                'timestamp': datetime.now().isoformat(),
                'archivos': archivos_copiados,
                'tamaño_total': tamaño_total,
                'tipo': 'incremental',
                'estado': 'completado'
            }
            
            with open(os.path.join(ruta_backup, 'metadata.json'), 'w') as f:
                json.dump(metadatos, f, indent=2, ensure_ascii=False)
            
            self.historial_sincronizacion.append(metadatos)
            self.guardar_historial()
            
            return metadatos
            
        except Exception as e:
            print(f"Error al crear backup incremental: {e}")
            return None
    
    def sincronizar_nube(self, servicio='local', archivos=[]):
        """
        Sincroniza datos con servicio en la nube
        
        Args:
            servicio: Servicio de nube (dropbox, google_drive, aws_s3, local)
            archivos: Archivos a sincronizar
        
        Returns:
            dict con resultado de sincronización
        """
        config = self.configuracion.get(servicio, {})
        
        if not config.get('habilitado'):
            return {
                'exitoso': False,
                'mensaje': f'Servicio {servicio} no habilitado',
                'servicio': servicio
            }
        
        if servicio == 'local':
            return self._sincronizar_local(archivos)
        elif servicio == 'dropbox':
            return self._sincronizar_dropbox(archivos)
        elif servicio == 'google_drive':
            return self._sincronizar_google_drive(archivos)
        elif servicio == 'aws_s3':
            return self._sincronizar_aws(archivos)
        else:
            return {
                'exitoso': False,
                'mensaje': f'Servicio desconocido: {servicio}'
            }
    
    def _sincronizar_local(self, archivos):
        """Sincronización local"""
        try:
            resultado = self.crear_backup_completo(archivos)
            return {
                'exitoso': True,
                'mensaje': 'Sincronización local completada',
                'servicio': 'local',
                'backup': resultado
            }
        except Exception as e:
            return {
                'exitoso': False,
                'mensaje': f'Error en sincronización local: {e}',
                'servicio': 'local'
            }
    
    def _sincronizar_dropbox(self, archivos):
        """Sincronización con Dropbox (simulada)"""
        return {
            'exitoso': False,
            'mensaje': 'Dropbox: Requiere configuración de token de autenticación',
            'servicio': 'dropbox',
            'instrucciones': 'Configura tu token de Dropbox en config_nube.json'
        }
    
    def _sincronizar_google_drive(self, archivos):
        """Sincronización con Google Drive (simulada)"""
        return {
            'exitoso': False,
            'mensaje': 'Google Drive: Requiere configuración de credenciales OAuth',
            'servicio': 'google_drive',
            'instrucciones': 'Configura tu Google API key en config_nube.json'
        }
    
    def _sincronizar_aws(self, archivos):
        """Sincronización con AWS S3 (simulada)"""
        return {
            'exitoso': False,
            'mensaje': 'AWS S3: Requiere configuración de credenciales AWS',
            'servicio': 'aws_s3',
            'instrucciones': 'Configura tus credenciales AWS en config_nube.json'
        }
    
    def restaurar_backup(self, nombre_backup, directorio_destino='.'):
        """
        Restaura datos desde un backup
        
        Args:
            nombre_backup: Nombre del backup a restaurar
            directorio_destino: Directorio donde restaurar
        
        Returns:
            dict con resultado de restauración
        """
        try:
            ruta_backup = os.path.join(self.directorio_local, nombre_backup)
            
            if not os.path.exists(ruta_backup):
                return {
                    'exitoso': False,
                    'mensaje': f'Backup no encontrado: {nombre_backup}'
                }
            
            # Restaurar archivos
            archivos_restaurados = []
            
            for archivo in os.listdir(ruta_backup):
                if archivo == 'metadata.json':
                    continue
                
                ruta_origen = os.path.join(ruta_backup, archivo)
                ruta_destino = os.path.join(directorio_destino, archivo)
                
                shutil.copy2(ruta_origen, ruta_destino)
                archivos_restaurados.append(archivo)
            
            return {
                'exitoso': True,
                'mensaje': 'Backup restaurado correctamente',
                'archivos_restaurados': archivos_restaurados,
                'cantidad': len(archivos_restaurados)
            }
            
        except Exception as e:
            return {
                'exitoso': False,
                'mensaje': f'Error al restaurar backup: {e}'
            }
    
    def listar_backups(self):
        """Lista todos los backups disponibles"""
        backups = []
        
        try:
            for carpeta in os.listdir(self.directorio_local):
                ruta_carpeta = os.path.join(self.directorio_local, carpeta)
                
                if os.path.isdir(ruta_carpeta):
                    metadata_file = os.path.join(ruta_carpeta, 'metadata.json')
                    
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            backups.append(metadata)
            
            # Ordenar por timestamp descendente
            backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return backups
            
        except Exception as e:
            print(f"Error al listar backups: {e}")
            return []
    
    def obtener_estadisticas_backups(self):
        """Obtiene estadísticas de los backups"""
        backups = self.listar_backups()
        
        if not backups:
            return {
                'total_backups': 0,
                'tamaño_total': 0,
                'tamaño_promedio': 0,
                'ultimo_backup': None
            }
        
        tamaño_total = sum(b.get('tamaño_total', 0) for b in backups)
        tamaño_promedio = tamaño_total / len(backups) if backups else 0
        
        return {
            'total_backups': len(backups),
            'tamaño_total': tamaño_total,
            'tamaño_promedio': tamaño_promedio,
            'ultimo_backup': backups[0].get('timestamp') if backups else None,
            'primer_backup': backups[-1].get('timestamp') if backups else None,
            'tipos_backup': {
                'completo': sum(1 for b in backups if b.get('tipo') == 'completo'),
                'incremental': sum(1 for b in backups if b.get('tipo') == 'incremental')
            }
        }
    
    def cargar_historial(self):
        """Carga historial de sincronizaciones"""
        try:
            archivo_historial = os.path.join(self.directorio_local, 'historial.json')
            if os.path.exists(archivo_historial):
                with open(archivo_historial, 'r') as f:
                    self.historial_sincronizacion = json.load(f)
        except Exception as e:
            print(f"Error al cargar historial: {e}")
    
    def guardar_historial(self):
        """Guarda historial de sincronizaciones"""
        try:
            archivo_historial = os.path.join(self.directorio_local, 'historial.json')
            with open(archivo_historial, 'w') as f:
                json.dump(self.historial_sincronizacion, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def limpiar_backups_antiguos(self, dias=30):
        """
        Elimina backups más antiguos que X días
        
        Args:
            dias: Número de días para mantener backups
        """
        from datetime import timedelta
        
        fecha_limite = (datetime.now() - timedelta(days=dias)).isoformat()
        backups_eliminados = []
        
        try:
            for carpeta in os.listdir(self.directorio_local):
                ruta_carpeta = os.path.join(self.directorio_local, carpeta)
                
                if os.path.isdir(ruta_carpeta):
                    metadata_file = os.path.join(ruta_carpeta, 'metadata.json')
                    
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            
                            if metadata.get('timestamp', '') < fecha_limite:
                                shutil.rmtree(ruta_carpeta)
                                backups_eliminados.append(carpeta)
            
            self.guardar_historial()
            
            return {
                'exitoso': True,
                'backups_eliminados': backups_eliminados,
                'cantidad': len(backups_eliminados)
            }
            
        except Exception as e:
            return {
                'exitoso': False,
                'mensaje': f'Error al limpiar backups: {e}'
            }


class MonitorSincronizacion:
    """Monitor para sincronización automática periódica"""
    
    def __init__(self, sincronizador):
        """
        Inicializa el monitor
        
        Args:
            sincronizador: Instancia de SincronizadorNube
        """
        self.sincronizador = sincronizador
        self.programaciones = []
        self.historial_ejecuciones = []
    
    def programar_sincronizacion(self, intervalo_minutos=60, archivos=None):
        """
        Programa sincronización automática
        
        Args:
            intervalo_minutos: Intervalo en minutos
            archivos: Archivos a sincronizar
        """
        programacion = {
            'id': len(self.programaciones) + 1,
            'intervalo_minutos': intervalo_minutos,
            'archivos': archivos or [],
            'proxima_ejecucion': datetime.now().isoformat(),
            'estado': 'activo'
        }
        
        self.programaciones.append(programacion)
        return programacion
    
    def obtener_programaciones(self):
        """Obtiene todas las programaciones"""
        return self.programaciones
    
    def detener_sincronizacion(self, id_programacion):
        """Detiene una sincronización programada"""
        for prog in self.programaciones:
            if prog['id'] == id_programacion:
                prog['estado'] = 'inactivo'
                return True
        return False


# Instancia global
sincronizador_nube = SincronizadorNube()
monitor_sincronizacion = MonitorSincronizacion(sincronizador_nube)
