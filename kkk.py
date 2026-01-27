import random
import re
from datetime import datetime

class SimpleIA:
    def __init__(self):
        self.nombre = "Anngpt"
        self.conversacion_historia = []
        
        # Base de conocimientos
        self.respuestas = {
            'saludo': [
                "¡Hola! ¿En qué puedo ayudarte?",
                "¡Hola! Es un placer hablar contigo.",
                "¡Saludos! ¿Qué necesitas?",
            ],
            'despedida': [
                "¡Hasta luego! Que tengas un excelente día.",
                "¡Adiós! Vuelve cuando quieras.",
                "¡Nos vemos! Fue un placer ayudarte.",
            ],
            'nombre': [
                f"Mi nombre es {self.nombre}. Soy una inteligencia artificial.",
                f"Me llamo {self.nombre}. ¿Y tú?",
                f"Soy {self.nombre}, tu asistente virtual.",
            ],
            'hora': [
                f"La hora actual es {datetime.now().strftime('%H:%M:%S')}",
            ],
            'fecha': [
                f"Hoy es {datetime.now().strftime('%d de %B de %Y')}",
            ],
            'ayuda': [
                "Puedo responder preguntas, hacer cálculos matemáticos, y mantener una conversación contigo.",
                "Estoy aquí para ayudarte. Puedo hablar sobre varios temas, hacer cálculos, y más.",
            ],
            'estado': [
                "¡Me siento genial! Gracias por preguntar.",
                "Estoy funcionando perfectamente. ¿Y tú cómo estás?",
                "Todo bien por aquí. ¿Cómo estás tú?",
            ],
            'default': [
                "Interesante. Cuéntame más.",
                "Entiendo. ¿Algo más que quieras compartir?",
                "Hmm, no estoy seguro de cómo responder a eso. ¿Puedes reformular?",
                "Es un tema interesante. ¿Qué más te gustaría saber?",
            ]
        }
        
        # Patrones de reconocimiento
        self.patrones = {
            'saludo': r'\b(hola|hey|buenos|buenas|saludos|qué tal)\b',
            'despedida': r'\b(adiós|adios|chao|hasta luego|bye|nos vemos)\b',
            'nombre': r'\b(tu nombre|cómo te llamas|quién eres|como te llamas)\b',
            'hora': r'\b(qué hora|hora es|dame la hora)\b',
            'fecha': r'\b(qué día|fecha|día es hoy)\b',
            'ayuda': r'\b(ayuda|ayúdame|qué puedes hacer|que puedes hacer)\b',
            'estado': r'\b(cómo estás|como estas|qué tal estas|todo bien)\b',
            'calculo': r'(\d+\s*[\+\-\*\/]\s*\d+)',
        }
    
    def procesar_texto(self, texto):
        """Procesa el texto de entrada y clasifica la intención"""
        texto = texto.lower()
        
        # Guardar en historial
        self.conversacion_historia.append(('usuario', texto))
        
        # Buscar patrones
        for categoria, patron in self.patrones.items():
            if re.search(patron, texto, re.IGNORECASE):
                if categoria == 'calculo':
                    respuesta = self.calcular(texto)
                else:
                    respuesta = random.choice(self.respuestas.get(categoria, self.respuestas['default']))
                
                self.conversacion_historia.append(('ia', respuesta))
                return respuesta
        
        # Si no se encuentra patrón, respuesta por defecto
        respuesta = random.choice(self.respuestas['default'])
        self.conversacion_historia.append(('ia', respuesta))
        return respuesta
    
    def calcular(self, texto):
        """Realiza cálculos matemáticos simples"""
        try:
            # Extraer la expresión matemática
            match = re.search(r'(\d+\s*[\+\-\*\/]\s*\d+)', texto)
            if match:
                expresion = match.group(1)
                # Evaluar de forma segura
                resultado = eval(expresion)
                return f"El resultado de {expresion} es {resultado}"
        except Exception as e:
            return "Lo siento, no pude realizar ese cálculo."
        
        return "No encontré una operación matemática válida."
    
    def mostrar_historial(self):
        """Muestra el historial de la conversación"""
        print("\n--- Historial de Conversación ---")
        for emisor, mensaje in self.conversacion_historia:
            if emisor == 'usuario':
                print(f"TÚ: {mensaje}")
            else:
                print(f"{self.nombre.upper()}: {mensaje}")
        print("-" * 35)
    
    def aprender(self, patron, respuestas):
        """Permite agregar nuevos patrones y respuestas"""
        self.patrones[patron] = patron
        self.respuestas[patron] = respuestas
        print(f"✓ He aprendido un nuevo patrón: {patron}")


def main():
    # Crear instancia de la IA
    ia = SimpleIA()
    
    print("=" * 50)
    print(f"  {ia.nombre} - Chatbot Inteligente")
    print("=" * 50)
    print("\n¡Hola! Soy tu asistente virtual.")
    print("Puedo conversar contigo, hacer cálculos, y más.")
    print("Escribe 'salir' para terminar la conversación.")
    print("Escribe 'historial' para ver nuestra conversación.\n")
    
    # Bucle principal
    while True:
        try:
            # Obtener entrada del usuario
            entrada = input("TÚ: ").strip()
            
            # Verificar salida
            if entrada.lower() in ['salir', 'exit', 'quit']:
                print(f"\n{ia.nombre.upper()}: {random.choice(ia.respuestas['despedida'])}")
                break
            
            # Mostrar historial
            if entrada.lower() == 'historial':
                ia.mostrar_historial()
                continue
            
            # Procesar y responder
            if entrada:
                respuesta = ia.procesar_texto(entrada)
                print(f"\n{ia.nombre.upper()}: {respuesta}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{ia.nombre.upper()}: ¡Hasta pronto!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
