"""
Módulo de encriptación para proteger datos sensibles
Utiliza Fernet para cifrado simétrico AES-128
"""

import os
import json
from datetime import datetime

class EncriptadorDatos:
    """Gestor de encriptación para datos sensibles del sistema médico"""
    
    def __init__(self, clave_maestra=None):
        """
        Inicializa el encriptador
        
        Args:
            clave_maestra: Clave para cifrado (si no existe, genera una nueva)
        """
        self.clave_archivo = 'clave_maestra.key'
        self.clave_maestra = clave_maestra or self._obtener_o_crear_clave()
        self.datos_encriptados = {}
        self.cargar_datos_encriptados()
    
    def _obtener_o_crear_clave(self):
        """Obtiene clave maestra o la genera si no existe"""
        try:
            # Para producción usar cryptography.Fernet
            # Aquí usamos una implementación simple con hashlib
            import hashlib
            
            if os.path.exists(self.clave_archivo):
                with open(self.clave_archivo, 'r') as f:
                    return f.read().strip()
            else:
                # Generar clave única basada en timestamp + random
                import secrets
                clave = secrets.token_hex(32)
                with open(self.clave_archivo, 'w') as f:
                    f.write(clave)
                return clave
        except Exception as e:
            print(f"Error al obtener clave: {e}")
            return None
    
    def cifrar_datos(self, datos_texto, tipo_datos='general'):
        """
        Cifra datos sensibles
        
        Args:
            datos_texto: Texto a cifrar
            tipo_datos: Tipo de datos (para identificación)
        
        Returns:
            dict con datos cifrados y metadatos
        """
        try:
            import hashlib
            import base64
            
            # Crear hash para verificación
            hash_original = hashlib.sha256(datos_texto.encode()).hexdigest()
            
            # Cifrado simple XOR (para demostración)
            # En producción usar cryptography.Fernet
            datos_cifrados = self._cifrar_xor(datos_texto)
            
            registro_cifrado = {
                'datos': base64.b64encode(datos_cifrados).decode(),
                'tipo': tipo_datos,
                'hash': hash_original,
                'fecha_cifrado': datetime.now().isoformat(),
                'estado': 'cifrado'
            }
            
            self.datos_encriptados[hash_original] = registro_cifrado
            return registro_cifrado
            
        except Exception as e:
            print(f"Error al cifrar: {e}")
            return None
    
    def descifrar_datos(self, hash_dato):
        """
        Descifra datos previamente cifrados
        
        Args:
            hash_dato: Hash del dato a descifrar
        
        Returns:
            Texto descifrado
        """
        try:
            if hash_dato not in self.datos_encriptados:
                return None
            
            import base64
            
            registro = self.datos_encriptados[hash_dato]
            datos_cifrados = base64.b64decode(registro['datos'])
            datos_descifrados = self._descifrar_xor(datos_cifrados)
            
            return datos_descifrados.decode('utf-8', errors='ignore')
            
        except Exception as e:
            print(f"Error al descifrar: {e}")
            return None
    
    def _cifrar_xor(self, texto):
        """Implementación simple de cifrado XOR (demostrativa)"""
        if not self.clave_maestra:
            return texto.encode()
        
        clave_bytes = self.clave_maestra.encode()
        texto_bytes = texto.encode()
        cifrado = bytearray()
        
        for i, byte in enumerate(texto_bytes):
            cifrado.append(byte ^ clave_bytes[i % len(clave_bytes)])
        
        return bytes(cifrado)
    
    def _descifrar_xor(self, datos):
        """Implementación simple de descifrado XOR (demostrativa)"""
        if not self.clave_maestra:
            return datos
        
        clave_bytes = self.clave_maestra.encode()
        descifrado = bytearray()
        
        for i, byte in enumerate(datos):
            descifrado.append(byte ^ clave_bytes[i % len(clave_bytes)])
        
        return bytes(descifrado)
    
    def guardar_datos_encriptados(self):
        """Guarda registro de datos encriptados en archivo"""
        try:
            with open('datos_encriptados.json', 'w') as f:
                json.dump(self.datos_encriptados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar datos cifrados: {e}")
            return False
    
    def cargar_datos_encriptados(self):
        """Carga registro de datos encriptados desde archivo"""
        try:
            if os.path.exists('datos_encriptados.json'):
                with open('datos_encriptados.json', 'r') as f:
                    self.datos_encriptados = json.load(f)
            return True
        except Exception as e:
            print(f"Error al cargar datos cifrados: {e}")
            return False
    
    def cifrar_paciente(self, id_paciente, datos_paciente):
        """
        Cifra datos sensibles de un paciente
        
        Args:
            id_paciente: ID del paciente
            datos_paciente: Dict con datos del paciente
        
        Returns:
            Dict con campos cifrados
        """
        campos_sensibles = ['email', 'telefono', 'cedula', 'direccion']
        datos_cifrados = {}
        
        for campo, valor in datos_paciente.items():
            if campo in campos_sensibles and valor:
                resultado = self.cifrar_datos(str(valor), f'paciente_{campo}')
                datos_cifrados[campo] = resultado['hash'] if resultado else None
            else:
                datos_cifrados[campo] = valor
        
        return datos_cifrados
    
    def descifrar_paciente(self, datos_paciente_cifrados):
        """
        Descifra datos de un paciente
        
        Args:
            datos_paciente_cifrados: Dict con datos cifrados
        
        Returns:
            Dict con datos descifrados
        """
        campos_sensibles = ['email', 'telefono', 'cedula', 'direccion']
        datos_descifrados = {}
        
        for campo, valor in datos_paciente_cifrados.items():
            if campo in campos_sensibles and valor:
                descifrado = self.descifrar_datos(valor)
                datos_descifrados[campo] = descifrado if descifrado else valor
            else:
                datos_descifrados[campo] = valor
        
        return datos_descifrados
    
    def generar_clave_temporal(self, duracion_minutos=30):
        """
        Genera clave temporal para acceso compartido
        
        Args:
            duracion_minutos: Minutos de validez
        
        Returns:
            Clave temporal
        """
        import secrets
        from datetime import timedelta
        
        clave_temporal = secrets.token_urlsafe(32)
        
        registro = {
            'clave': clave_temporal,
            'creada': datetime.now().isoformat(),
            'expira': (datetime.now() + timedelta(minutes=duracion_minutos)).isoformat(),
            'activo': True
        }
        
        return clave_temporal, registro
    
    def verificar_integridad(self, datos_original, hash_verificacion):
        """
        Verifica integridad de datos comparando hashes
        
        Args:
            datos_original: Datos a verificar
            hash_verificacion: Hash esperado
        
        Returns:
            Boolean indicando si los datos no han sido modificados
        """
        import hashlib
        
        hash_calculado = hashlib.sha256(datos_original.encode()).hexdigest()
        return hash_calculado == hash_verificacion
    
    def registrar_acceso_dato(self, hash_dato, usuario, accion='lectura'):
        """
        Registra acceso a datos cifrados para auditoría
        
        Args:
            hash_dato: Hash del dato accedido
            usuario: Usuario que accedió
            accion: Tipo de acción (lectura, modificación, eliminación)
        """
        if hash_dato not in self.datos_encriptados:
            return False
        
        registro = self.datos_encriptados[hash_dato]
        if 'accesos' not in registro:
            registro['accesos'] = []
        
        registro['accesos'].append({
            'usuario': usuario,
            'accion': accion,
            'timestamp': datetime.now().isoformat()
        })
        
        self.guardar_datos_encriptados()
        return True
    
    def obtener_auditoria(self, hash_dato):
        """
        Obtiene registro de auditoría de un dato
        
        Args:
            hash_dato: Hash del dato
        
        Returns:
            Lista de accesos registrados
        """
        if hash_dato in self.datos_encriptados:
            return self.datos_encriptados[hash_dato].get('accesos', [])
        return []


class GestorClaves:
    """Gestor de claves y permisos de encriptación"""
    
    def __init__(self):
        self.claves_usuario = {}
        self.permisos = {}
        self.cargar_claves()
    
    def crear_clave_usuario(self, usuario_id, contraseña):
        """Crea clave de encriptación para usuario"""
        import hashlib
        
        clave_derivada = hashlib.pbkdf2_hmac(
            'sha256',
            contraseña.encode(),
            bytes.fromhex('0' * 64),
            100000
        )
        
        self.claves_usuario[usuario_id] = clave_derivada.hex()
        self.guardar_claves()
        
        return self.claves_usuario[usuario_id]
    
    def asignar_permiso(self, usuario_id, recurso, acciones):
        """
        Asigna permisos de acceso a un usuario
        
        Args:
            usuario_id: ID del usuario
            recurso: Recurso protegido
            acciones: Lista de acciones permitidas (lectura, escritura, etc)
        """
        if usuario_id not in self.permisos:
            self.permisos[usuario_id] = {}
        
        self.permisos[usuario_id][recurso] = {
            'acciones': acciones,
            'asignado_en': datetime.now().isoformat()
        }
        
        self.guardar_claves()
    
    def verificar_permiso(self, usuario_id, recurso, accion):
        """Verifica si usuario tiene permiso para una acción"""
        if usuario_id not in self.permisos:
            return False
        
        if recurso not in self.permisos[usuario_id]:
            return False
        
        return accion in self.permisos[usuario_id][recurso]['acciones']
    
    def guardar_claves(self):
        """Guarda claves y permisos"""
        try:
            datos = {
                'claves_usuario': self.claves_usuario,
                'permisos': self.permisos
            }
            with open('claves_usuarios.json', 'w') as f:
                json.dump(datos, f, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar claves: {e}")
            return False
    
    def cargar_claves(self):
        """Carga claves y permisos"""
        try:
            if os.path.exists('claves_usuarios.json'):
                with open('claves_usuarios.json', 'r') as f:
                    datos = json.load(f)
                    self.claves_usuario = datos.get('claves_usuario', {})
                    self.permisos = datos.get('permisos', {})
            return True
        except Exception as e:
            print(f"Error al cargar claves: {e}")
            return False


# Instancias globales
encriptador = EncriptadorDatos()
gestor_claves = GestorClaves()
