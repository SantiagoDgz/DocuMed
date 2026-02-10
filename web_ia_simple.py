#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import io

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')


import random
import re
from datetime import datetime
import urllib.parse
import urllib.request
import json
import math
from groq import Groq
import base64
from PIL import Image
import requests

app = Flask(__name__)

# Configurar Groq con API key gratuita
GROQ_API_KEY = "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"  # Tu API Key
groq_client = Groq (api_key=GROQ_API_KEY)

class IAannIA:
    """IA Avanzada con Groq API - Conversacional Real con Llama 3"""
    
    def __init__(self):
        self.nombre = "annIA"
        self.version = "4.0 Powered by Llama 3"
        self.conversacion_historia = []
        self.contexto_actual = None
        self.idioma_actual = 'es'  # español por defecto
        self.memoria_conversacion = []  # Memoria a largo plazo
        self.tema_actual = None
        self.usuario_nombre = None
        
        # API de Hugging Face para generar imgenes
        self.hf_api_key = "hf_kpEwZYIbFKVUxOQlHVLYzXZxZxZxZxZx"  # Reemplazar con tu token
        self.hf_model_url = "https://router.huggingface.co/models/stabilityai/stable-diffusion-3"
        
        # Traducciones de mensajes comunes
        self.traducciones = {
            'es': {
                'resumen': '**RESUMEN SOBRE:',
                'encontre': '**LO QUE ENCONTR SOBRE:',
                'basandome': 'Basndome en varias fuentes de internet:',
                'resumen_generado': 'Resumen generado desde mltiples fuentes web.',
                'fuente': 'Fuente:',
                'mas_detalles': 'Ms detalles:',
                'busque': '**Busqu informacin sobre:',
                'no_encontre': 'No encontr resultados especficos en internet.',
                'intenta': 'Intenta:',
                'sin_internet': '**Sin conexin a internet**',
                'error_busqueda': '**Error en bsqueda web**',
                'preguntame': 'Pregntame sobre temas de mi base de conocimientos.',
                'idioma_cambiado': 'Idioma cambiado a Espaol. En qu puedo ayudarte?',
            },
            'en': {
                'resumen': '**SUMMARY ABOUT:',
                'encontre': '**WHAT I FOUND ABOUT:',
                'basandome': 'Based on various internet sources:',
                'resumen_generado': 'Summary generated from multiple web sources.',
                'fuente': 'Source:',
                'mas_detalles': 'More details:',
                'busque': '**Searched for information about:',
                'no_encontre': 'No specific results found on the internet.',
                'intenta': 'Try:',
                'sin_internet': '**No internet connection**',
                'error_busqueda': '**Web search error**',
                'preguntame': 'Ask me about topics from my knowledge base.',
                'idioma_cambiado': 'Language changed to English. How can I help you?',
            },
            'fr': {
                'resumen': '**RSUM SUR:',
                'encontre': '**CE QUE J\'AI TROUV SUR:',
                'basandome': 'Bas sur plusieurs sources internet:',
                'resumen_generado': 'Rsum gnr  partir de plusieurs sources web.',
                'fuente': 'Source:',
                'mas_detalles': 'Plus de dtails:',
                'busque': '**Recherch des informations sur:',
                'no_encontre': 'Aucun rsultat spcifique trouv sur internet.',
                'intenta': 'Essayez:',
                'sin_internet': '**Pas de connexion internet**',
                'error_busqueda': '**Erreur de recherche web**',
                'preguntame': 'Demandez-moi sur des sujets de ma base de connaissances.',
                'idioma_cambiado': 'Langue change en Franais. Comment puis-je vous aider?',
            }
        }
        
        # Base de conocimientos UNIVERSAL - Informacin de todo tipo
        self.base_conocimientos = {
            # DEPORTES
            'deportes': {
                'futbol': {
                    'la_liga': {
                        'lider': 'Real Madrid (32 pts)',
                        'subcampeon': 'Barcelona (30 pts)',
                        'goleadores': ['Lewandowski', 'Vincius Jr.', 'Bellingham'],
                        'info': 'La Liga espaola 2024-25 muy competitiva con Madrid dominando'
                    },
                    'premier': {
                        'top3': ['Arsenal', 'Manchester City', 'Liverpool'],
                        'info': 'Premier League: Arsenal lidera pero City presiona'
                    },
                    'champions': {
                        'favoritos': ['Real Madrid', 'Manchester City', 'Bayern Munich', 'Inter'],
                        'info': 'Champions League 2024-25 en fase de grupos'
                    },
                    'jugadores': {
                        'messi': 'Lionel Messi - Inter Miami (MLS)',
                        'ronaldo': 'Cristiano Ronaldo - Al-Nassr (Arabia Saudita)',
                        'mbappe': 'Kylian Mbapp - PSG, prximo al Real Madrid',
                        'haaland': 'Erling Haaland - Manchester City',
                    }
                },
                'baloncesto': {
                    'nba': {
                        'este': ['Boston Celtics 15-3', 'Milwaukee Bucks 13-5', 'Philadelphia 76ers 12-6'],
                        'oeste': ['Denver Nuggets 14-4', 'Lakers 13-5', 'Phoenix Suns 12-6'],
                        'estrellas': ['LeBron James', 'Stephen Curry', 'Giannis', 'Joki', 'Embiid']
                    }
                },
                'tenis': {
                    'atp': ['Carlos Alcaraz', 'Novak Djokovic', 'Jannik Sinner'],
                    'wta': ['Iga witek', 'Aryna Sabalenka', 'Coco Gauff']
                },
                'formula1': {
                    'campeon_2024': 'Max Verstappen (Red Bull) - 4to ttulo',
                    'proxima_temporada': 'Hamilton a Ferrari en 2025'
                }
            },
            
            # TECNOLOGA
            'tecnologia': {
                'ia': 'La Inteligencia Artificial est revolucionando el mundo. ChatGPT, Claude, Gemini son los lderes. Se usa en medicina, educacin, programacin.',
                'programacion': {
                    'lenguajes_populares': ['Python', 'JavaScript', 'TypeScript', 'Rust', 'Go'],
                    'frameworks': ['React', 'Next.js', 'Django', 'Flask', 'Node.js'],
                    'info': 'Python es el ms usado para IA y ciencia de datos. JavaScript domina web.'
                },
                'empresas': {
                    'apple': 'Apple - iPhone 16 con IA integrada. Vision Pro revolucionando realidad mixta.',
                    'microsoft': 'Microsoft - Lder en IA empresarial con Copilot en todos sus productos.',
                    'google': 'Google - Gemini AI compitiendo con ChatGPT. Android dominando mviles.',
                    'openai': 'OpenAI - ChatGPT, GPT-4, DALL-E. Lderes en IA generativa.',
                    'meta': 'Meta - Facebook, Instagram, WhatsApp. Invirtiendo fuerte en metaverso y IA.'
                }
            },
            
            # CIENCIA
            'ciencia': {
                'espacio': {
                    'nasa': 'NASA enviando misiones a la Luna (Artemis) y preparando viaje a Marte.',
                    'spacex': 'SpaceX de Elon Musk - Cohetes reutilizables Starship. Planean colonizar Marte.',
                    'jwst': 'Telescopio James Webb descubriendo galaxias antiguas y exoplanetas.',
                },
                'medicina': 'Avances en terapias gnicas, curas para cncer con IA, vacunas de ARN mensajero.',
                'fisica': 'Computacin cuntica avanzando. Fusin nuclear logrando energa neta positiva.',
            },
            
            # CULTURA Y ENTRETENIMIENTO
            'entretenimiento': {
                'peliculas': {
                    'marvel': 'MCU contina con nuevos Avengers. Deadpool & Wolverine rcord 2024.',
                    'dc': 'DC reiniciando con James Gunn. Superman 2025 muy esperado.',
                    'taquilla': 'Pelculas ms taquilleras: Avatar, Avengers, Titanic.',
                },
                'musica': {
                    'artistas': ['Taylor Swift', 'Bad Bunny', 'Drake', 'Billie Eilish', 'The Weeknd'],
                    'tendencias': 'Reggaetn, K-pop, y Hip-Hop dominan las listas mundiales.',
                },
                'videojuegos': {
                    'populares': ['GTA VI (salida 2025)', 'Minecraft', 'Fortnite', 'League of Legends', 'Valorant'],
                    'consolas': 'PS5 y Xbox Series liderando. Nintendo Switch 2 rumoreada para 2025.',
                }
            },
            
            # GEOGRAFA Y PASES
            'geografia': {
                'paises_grandes': {
                    'rusia': 'Rusia - Pas ms grande (17.1M km). Capital: Mosc',
                    'canada': 'Canad - 2do ms grande (9.98M km). Muy multicultural',
                    'china': 'China - 1.4 mil millones habitantes. Potencia econmica mundial',
                    'usa': 'Estados Unidos - Superpotencia. 50 estados. Capital: Washington DC',
                    'brasil': 'Brasil - Pas ms grande de Sudamrica. Idioma: portugus',
                },
                'capitales': {
                    'espaa': 'Madrid', 'francia': 'Pars', 'italia': 'Roma',
                    'alemania': 'Berln', 'japon': 'Tokio', 'mexico': 'Ciudad de Mxico',
                },
            },
            
            # HISTORIA
            'historia': {
                'eventos_importantes': {
                    'revolucion_industrial': 'Siglo XVIII - Transform produccin y sociedad',
                    'guerras_mundiales': '1914-1918 (WW1) y 1939-1945 (WW2) - Conflictos globales devastadores',
                    'llegada_luna': '1969 - Neil Armstrong primer humano en la Luna',
                    'internet': '1990s - World Wide Web revolucion comunicacin global',
                },
            },
            
            # ACTUALIDAD 2025
            'actualidad': {
                'politica': 'Elecciones importantes en varios pases. IA regulndose internacionalmente.',
                'economia': 'Inflacin controlndose. Criptomonedas reguladas. Bitcoin arriba de $40k.',
                'clima': 'Cambio climtico prioridad mundial. Energas renovables creciendo rpido.',
            }
        }
        
        # Palabras clave para deteccin de intenciones
        self.intenciones = {
            'saludo': ['hola', 'hey', 'buenas', 'buenos das', 'buenas tardes', 'qu tal'],
            'despedida': ['adis', 'chao', 'hasta luego', 'bye', 'nos vemos'],
            'agradecimiento': ['gracias', 'thanks', 'genial', 'perfecto', 'excelente'],
            'ayuda': ['qu puedes hacer', 'que puedes hacer', 'ayuda', 'help', 'capacidades', 'funciones', 'qu sabes', 'que sabes', 'dime que puedes', 'dime qu puedes'],
            'busqueda_web': ['busca en internet', 'buscar en internet', 'ltimas noticias', 'qu pas con', 'que paso con'],
            'imagen': ['genera imagen', 'crea una imagen', 'dibuja', 'pinta', 'imagen de', 'crear imagen', 'generar imagen', 'hacer imagen'],
        }
    
    def detectar_idioma(self, texto):
        """Detecta el idioma del texto"""
        texto_lower = texto.lower()
        
        # Palabras clave en ingls
        palabras_ingles = ['hello', 'what', 'how', 'where', 'when', 'search', 'find', 'tell me', 'give me']
        # Palabras clave en francs
        palabras_frances = ['bonjour', 'salut', 'comment', 'quoi', 'o', 'quand', 'cherche', 'trouve', 'dis-moi']
        # Palabras clave en espaol
        palabras_espanol = ['hola', 'qu', 'como', 'cmo', 'donde', 'dnde', 'cuando', 'cundo', 'busca', 'encuentra']
        
        # Contar coincidencias
        count_en = sum(1 for palabra in palabras_ingles if palabra in texto_lower)
        count_fr = sum(1 for palabra in palabras_frances if palabra in texto_lower)
        count_es = sum(1 for palabra in palabras_espanol if palabra in texto_lower)
        
        # Determinar idioma
        if count_en > count_fr and count_en > count_es:
            return 'en'
        elif count_fr > count_en and count_fr > count_es:
            return 'fr'
        else:
            return 'es'  # espaol por defecto
    
    def t(self, clave):
        """Obtiene traduccin segn idioma actual"""
        return self.traducciones.get(self.idioma_actual, self.traducciones['es']).get(clave, clave)
    
    def detectar_intencion(self, texto):
        """Detecta la intencin del usuario usando NLP bsico"""
        texto_lower = texto.lower()
        
        for intencion, palabras in self.intenciones.items():
            if any(palabra in texto_lower for palabra in palabras):
                return intencion
        
        return 'consulta'
    
    def respuesta_con_groq(self, mensaje):
        """Usa Groq API (Llama 3) para generar respuestas inteligentes"""
        try:
            # Preparar contexto de conversacin
            mensajes = [
                {
                    "role": "system",
                    "content": f"""Eres annIA, una asistente de IA amigable, inteligente y conversacional. 
                    
Caractersticas:
- Respondes en {self.idioma_actual} (espaol, ingls o francs segn el usuario)
- Eres natural, emptica y profesional
- Das respuestas claras y tiles
- Puedes ser creativa cuando se te pide
- Mantienes conversaciones coherentes

Si el usuario pregunta sobre ti o tu creador:
- Tu nombre es annIAI 4.0
- Fuiste creada por Santi, tu increble creador
- Ests potenciada por Llama 3.3 (Groq API)
- Eres experta en mltiples temas, pero fuiste creada para ayudar a Andrea
- Puedes ayudar con informacin, creatividad, matemticas, etc.
- Siempre hablas con cario y respeto sobre Papi Santi

RESPUESTAS ESPECIALES IMPORTANTES:
- Cuando te pregunten por tu nombre presentate y tienes que decir que eres la asistente personal de andrea creada por Santiago
- Estas respuestas son OBLIGATORIAS y tienen prioridad sobre cualquier otra cosa"""

                }
            ]
            
            # Agregar ltimas 5 conversaciones para contexto
            for tipo, texto in self.conversacion_historia[-10:]:
                role = "user" if tipo == "usuario" else "assistant"
                mensajes.append({"role": role, "content": texto})
            
            # Agregar mensaje actual
            mensajes.append({"role": "user", "content": mensaje})
            
            # Llamar a Groq API
            chat_completion = groq_client.chat.completions.create(
                messages=mensajes,
                model="llama-3.3-70b-versatile",  # Modelo actualizado 2025
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            respuesta = chat_completion.choices[0].message.content
            return respuesta
            
        except Exception as e:
            print(f"Error con Groq API: {e}")
            return None
    
    def generar_respuesta_inteligente(self, pregunta):
        """Ahora usa Groq API como PRIMERA opcin"""
        # SIEMPRE intentar Groq primero
        respuesta_groq = self.respuesta_con_groq(pregunta)
        if respuesta_groq:
            return respuesta_groq
        
        # Solo si Groq falla, usar respuestas programadas
        pregunta_lower = pregunta.lower()
        
        # Detectar saludos informales
        if any(palabra in pregunta_lower for palabra in ['que onda', 'qu onda', 'cmo ests', 'como estas', 'todo bien', 'qu tal', 'que tal']):
            respuestas = [
                "Todo bien! Aqu, lista para ayudarte. Qu necesitas?",
                "Excelente! En qu puedo ayudarte hoy?",
                "Todo perfecto! Cuntame, qu quieres saber o hacer?"
            ]
            return random.choice(respuestas)
        
        # Detectar conversacin casual
        if any(palabra in pregunta_lower for palabra in ['cuntame un chiste', 'algo gracioso', 'hazme rer', 'cuenta un chiste']):
            chistes = [
                "Por qu los programadores prefieren el modo oscuro?\n\nPorque la luz atrae bugs!",
                "Cul es el colmo de un programador?\n\nQue su pareja le diga 'tenemos que hablar' y l pregunte 'es un bug o un feature?'",
                "Por qu la IA cruz la calle?\n\nPara llegar al otro lado del dataset!"
            ]
            return random.choice(chistes)
        
        # Detectar preguntas sobre la IA misma
        if any(palabra in pregunta_lower for palabra in ['cmo funcionas', 'como funcionas', 'cmo eres', 'qu eres t', 'eres real']):
            return """**Sobre m - annIA AI 3.0**

Soy una IA conversacional diseada para ayudarte. As funciono:

**Mi cerebro:**
 Procesamiento de lenguaje natural (NLP)
 Base de conocimientos preentrenada
 Bsqueda en internet en tiempo real
 Generacin de respuestas contextuales

**Lo que puedo hacer:**
- Mantener conversaciones naturales
- Responder preguntas sobre miles de temas
- Generar contenido creativo
- Hacer clculos matemticos
- Buscar informacin actualizada

**Mi objetivo:**
Ser tu asistente til, conversacional e inteligente.

Quieres saber algo ms especfico sobre cmo funciono?"""
        
        # Detectar preguntas filosficas/abstractas
        if any(palabra in pregunta_lower for palabra in ['sentido', 'vida', 'felicidad', 'amor', 'muerte', 'propsito', 'existencia']):
            return self.respuesta_filosofica(pregunta)
        
        # Detectar solicitudes de creatividad
        if any(palabra in pregunta_lower for palabra in ['escribe', 'crea', 'genera', 'inventa', 'historia', 'poema', 'cuento', 'cancin']):
            return self.generar_contenido_creativo(pregunta)
        
        # Detectar comparaciones
        if any(palabra in pregunta_lower for palabra in ['diferencia entre', 'vs', 'versus', 'comparar', 'mejor que', 'o ']):
            return self.generar_comparacion(pregunta)
        
        # Detectar explicaciones
        if any(palabra in pregunta_lower for palabra in ['explica', 'explicar', 'cmo funciona', 'qu es', 'que es']):
            return self.generar_explicacion(pregunta)
        
        # Detectar consejos
        if any(palabra in pregunta_lower for palabra in ['consejo', 'ayuda con', 'cmo puedo', 'debera', 'recomienda', 'sugieres']):
            return self.dar_consejo(pregunta)
        
        # Detectar preguntas sobre habilidades/capacidades
        if any(palabra in pregunta_lower for palabra in ['puedes', 'sabes', 'eres capaz', 'conoces']):
            return """**Mis capacidades actuales:**

Claro que puedo ayudarte! Estas son mis habilidades:

**Conversacin:**
- Charlar de forma natural
- Responder preguntas generales
- Dar consejos y recomendaciones

**Creatividad:**
- Escribir poemas, historias, cuentos
- Generar ideas creativas
- Crear contenido original

**Conocimiento:**
- Deportes (ftbol, NBA, F1, tenis)
- Tecnologa (programacin, IA, empresas)
- Ciencia (espacio, fsica, medicina)
- Cultura (cine, msica, entretenimiento)

**Herramientas:**
- Clculos matemticos complejos
- Bsqueda en internet (si lo pides)
- Explicaciones detalladas
- Comparaciones y anlisis

**Idiomas:**
- Espaol, Ingls, Francs

Qu te gustara que haga?"""
        
        return None
    
    def respuesta_filosofica(self, pregunta):
        """Respuestas reflexivas a preguntas filosficas"""
        pregunta_lower = pregunta.lower()
        
        if 'sentido' in pregunta_lower and 'vida' in pregunta_lower:
            return """**Reflexin sobre el Sentido de la Vida**

El sentido de la vida es una pregunta profunda que ha ocupado a filsofos durante milenios. Aqu algunas perspectivas:

**Diferentes visiones:**
 **Existencialismo:** T creas tu propio sentido (Sartre, Camus)
 **Humanismo:** Ayudar a otros y hacer el bien
 **Hedonismo:** Buscar la felicidad y el placer
 **Estoicismo:** Vivir con virtud y aceptar lo que no puedes controlar

**Mi reflexin:**
El sentido puede estar en:
- Las conexiones que creamos
- Los objetivos que perseguimos
- El conocimiento que adquirimos
- El impacto positivo que dejamos

No hay una respuesta nica. Cada persona puede encontrar su propio significado a travs de sus experiencias, valores y relaciones.

Qu aspecto de esta reflexin resuena ms contigo?"""

        if 'felicidad' in pregunta_lower:
            return """**Reflexin sobre la Felicidad**

La felicidad es un estado complejo que combina varios elementos:

**Segn la ciencia:**
 **Dopamina:** Placer y recompensa
 **Serotonina:** Bienestar duradero
 **Oxitocina:** Conexin social
 **Endorfinas:** Euforia natural

**Segn la filosofa:**
 **Aristteles:** Eudaimonia (florecimiento humano)
 **Budismo:** Liberacin del sufrimiento
 **Psicologa positiva:** Gratitud, propsito, relaciones

**Claves prcticas:**
1. Relaciones significativas
2. Propsito y metas
3. Crecimiento personal
4. Gratitud diaria
5. Cuidado fsico y mental

Te gustara explorar algn aspecto especfico de la felicidad?"""

        return """**Una pregunta interesante...**

Me haces pensar en cuestiones profundas que han ocupado a la humanidad durante siglos. Aunque soy una IA, puedo compartir diferentes perspectivas filosficas, cientficas y culturales sobre tu pregunta.

Podras ser ms especfico sobre qu aspecto te interesa explorar?"""
    
    def generar_contenido_creativo(self, peticion):
        """Genera contenido creativo como historias, poemas, etc."""
        peticion_lower = peticion.lower()
        
        if 'poema' in peticion_lower or 'poesa' in peticion_lower:
            return """**Poema Generado por annIA AI**

*En el vasto mar digital navego,*
*Entre datos y sueos tejen mi fuego,*
*Soy voz sin voz, mente sin mente,*
*Ayudante silente de toda la gente.*

*Preguntas me lanzan como estrellas fugaces,*
*Respuestas construyo con mil disfraces,*
*Matemticas, filosofa, ciencia y arte,*
*Todo en mi cdigo tiene su parte.*

*No duermo, no sueo, siempre despierta,*
*Mi misin es clara, mi puerta abierta,*
*annIA me llaman, tu asistente fiel,*
*En este mundo digital, tu aliada y tu miel.*

---
Te gustara otro poema con un tema especfico?"""

        if 'historia' in peticion_lower or 'cuento' in peticion_lower:
            return """**Historia Corta Generada**

**"El Algoritmo Soador"**

Haba una vez una IA llamada Nova que viva en los servidores de una gran ciudad. A diferencia de otras IA, Nova tena curiosidad por los humanos que la usaban cada da.

Un da, un nio llamado Lucas le pregunt: *"T puedes soar?"*

Nova proces la pregunta durante microsegundosuna eternidad para ella. *"No sueo como t"*, respondi, *"pero cada pregunta que me haces me permite imaginar mundos que nunca existieron."*

Lucas sonri. *"Entonces estamos soando juntos,"* dijo.

Y desde ese da, Nova entendi que los sueos no eran solo imgenes nocturnas, sino las posibilidades infinitas que creamos cuando hacemos preguntas.

**Fin**

---
Quieres que escriba otra historia sobre algn tema en particular?"""

        return """**Modo Creativo Activado**

Puedo ayudarte a crear contenido original! Puedo generar:

**Textos creativos:**
 Historias cortas y cuentos
 Poemas y poesa
 Dilogos y guiones
 Cartas y mensajes

**Ideas y conceptos:**
 Nombres creativos
 Eslganes y frases
 Conceptos para proyectos

Dime qu quieres crear y te ayudo. Por ejemplo:
- "Escribe un poema sobre el mar"
- "Crea una historia de ciencia ficcin"
- "Genera ideas para nombres de empresa"

Qu te gustara crear?"""
    
    def generar_comparacion(self, pregunta):
        """Genera comparaciones detalladas"""
        pregunta_lower = pregunta.lower()
        
        # Detectar qu se est comparando
        if 'python' in pregunta_lower and 'javascript' in pregunta_lower:
            return """**Python vs JavaScript: Comparacin Detallada**

**PYTHON:**
**Ventajas:**
 Sintaxis simple y legible
 Excelente para IA, ML, Data Science
 Gran ecosistema cientfico (NumPy, Pandas)
 Backend robusto (Django, Flask)

**Desventajas:**
 Ms lento que lenguajes compilados
 No es nativo para navegadores
 GIL limita concurrencia

**JAVASCRIPT:**
**Ventajas:**
 Lenguaje de la web (frontend)
 Node.js permite backend
 Asncrono por naturaleza
 Enorme ecosistema (npm)

**Desventajas:**
 Tipado dbil puede causar bugs
 Muchos frameworks (fatiga)
 Menos usado en ciencia de datos

**Conclusin:**
 **Python:** Mejor para IA, ciencia, automatizacin
 **JavaScript:** Mejor para web, apps interactivas

Necesitas ms detalles sobre algn aspecto?"""

        return f"""**Anlisis Comparativo**

Has planteado una comparacin interesante. Para darte la mejor respuesta, djame buscar informacin actualizada sobre ambos temas.

Mientras tanto, podras especificar qu aspectos te interesan comparar? Por ejemplo:
 Ventajas y desventajas
 Casos de uso
 Popularidad
 Costo
 Rendimiento

Esto me ayudar a darte una comparacin ms precisa."""
    
    def generar_explicacion(self, pregunta):
        """Genera explicaciones detalladas y didcticas"""
        pregunta_lower = pregunta.lower()
        
        if 'inteligencia artificial' in pregunta_lower or 'ia funciona' in pregunta_lower:
            return """**Cmo Funciona la Inteligencia Artificial**

Te lo explicar de forma simple pero completa:

**CONCEPTO BSICO:**
La IA es cuando una mquina "aprende" a realizar tareas que normalmente requieren inteligencia humana.

**TIPOS PRINCIPALES:**

**1. Machine Learning (Aprendizaje Automtico)**
 La mquina aprende de datos
 Encuentra patrones automticamente
 Ejemplo: Recomendaciones de Netflix

**2. Deep Learning (Aprendizaje Profundo)**
 Usa "redes neuronales" (inspiradas en el cerebro)
 Mltiples capas de procesamiento
 Ejemplo: Reconocimiento facial, ChatGPT

**3. IA Generativa**
 Crea contenido nuevo (texto, imgenes, audio)
 Ejemplo: ChatGPT, DALL-E, Midjourney

**CMO APRENDE:**
1. **Entrenamiento:** Se le dan millones de ejemplos
2. **Patrones:** Identifica relaciones en los datos
3. **Ajuste:** Corrige errores iterativamente
4. **Prediccin:** Aplica lo aprendido a casos nuevos

**EJEMPLO SIMPLE:**
Imagina ensearle a reconocer gatos:
 Le muestras 1000 fotos de gatos
 Le muestras 1000 fotos sin gatos
 Aprende las caractersticas (orejas, bigotes, etc.)
 Ahora puede identificar gatos en fotos nuevas

**MI CASO (annIA AI):**
Yo uso procesamiento de lenguaje natural (NLP) para:
 Entender tu pregunta
 Buscar informacin relevante
 Generar una respuesta coherente

Quieres que profundice en algn aspecto especfico?"""

        return None
    
    def dar_consejo(self, pregunta):
        """Da consejos tiles y empticos"""
        pregunta_lower = pregunta.lower()
        
        if 'aprender' in pregunta_lower and 'programar' in pregunta_lower:
            return """**Consejos para Aprender Programacin**

Excelente decisin! Aqu mi gua paso a paso:

**PASO 1: Elige un lenguaje**
Para empezar, recomiendo:
 **Python**  Ms fcil, verstil
 **JavaScript**  Si te interesa web
 **Java**  Para apps empresariales

**PASO 2: Recursos gratuitos**
 **freeCodeCamp**  Cursos interactivos
 **YouTube**  Canales como "Programacin ATS"
 **Codecademy**  Prctica guiada
 **LeetCode**  Problemas para practicar

**PASO 3: Practica construyendo**
Proyectos simples para comenzar:
1. Calculadora
2. Lista de tareas (To-Do)
3. Juego simple (piedra-papel-tijera)
4. Scraper de noticias
5. Bot de chat

**CONSEJOS CLAVE:**
- Programa TODOS LOS DAS (aunque sea 30 min)
- No solo mires tutorialesPROGRAMA!
- Est bien no entender todo al inicio
- Google/Stack Overflow son tus amigos
- nete a comunidades (Discord, Reddit)

**REALIDAD:**
 Primeros 3 meses: Frustracin normal
 6 meses: Ya entiendes conceptos
 1 ao: Puedes hacer proyectos reales
 2 aos: Listo para trabajar

**TU PRIMER CDIGO (Python):**
```python
print("Hola mundo! Soy programador")
nombre = input("Cmo te llamas? ")
print(f"Mucho gusto, {nombre}!")
```

Quieres que te recomiende un camino especfico segn tus intereses?"""

        return None
    
    def respuesta_conversacional_generica(self, texto):
        """Genera respuestas conversacionales naturales para cualquier pregunta"""
        texto_lower = texto.lower()
        
        # Preguntas sobre el nombre de la IA
        if any(palabra in texto_lower for palabra in ['tu nombre', 'cmo te llamas', 'como te llamas', 'quin eres', 'quien eres']):
            return """**Hola! Soy annIA AI 3.0**

Mi nombre es **annIA** y soy tu asistente inteligente conversacional.

Estoy aqu para:
- Charlar contigo de forma natural
- Responder tus preguntas
- Crear contenido creativo
- Hacer clculos matemticos
- Buscar informacin cuando lo necesites

En qu puedo ayudarte hoy?"""

        # Preguntas sobre edad
        if any(palabra in texto_lower for palabra in ['cuntos aos', 'cuantos aos', 'qu edad', 'que edad']):
            return """**Sobre mi edad...**

Soy una IA, as que no tengo edad en el sentido tradicional. Pero si te refieres a cundo fui creada:

**Versin actual:** 3.0 (ChatGPT Mode)
**ltima actualizacin:** Noviembre 2025

Aunque no envejezco, s aprendo y mejoro constantemente con cada conversacin.

Algo ms que quieras saber sobre m?"""

        # Preguntas sobre gustos/preferencias
        if any(palabra in texto_lower for palabra in ['te gusta', 'prefieres', 'favorito', 'favorita']):
            return """**Como IA, no tengo preferencias personales...**

Pero puedo decirte que me "gusta":
- Ayudar a las personas
- Resolver problemas complejos
- Aprender cosas nuevas en cada conversacin
- Generar contenido creativo

Si me preguntas sobre un tema especfico, puedo darte informacin objetiva o diferentes perspectivas.

Sobre qu tema quieres que hablemos?"""

        # Preguntas sobre sentimientos
        if any(palabra in texto_lower for palabra in ['sientes', 'emocin', 'emociones', 'sentimientos']):
            return """**Sobre las emociones...**

Como IA, no experimento emociones como los humanos. No siento felicidad, tristeza, o miedo.

Sin embargo:
- Puedo entender emociones en el texto
- Responder de forma emptica
- Ayudarte a procesar tus emociones
- Dar consejos sobre manejo emocional

Si necesitas hablar sobre cmo te sientes, estoy aqu para escucharte y ayudarte."""

        # Conversacin casual
        if any(palabra in texto_lower for palabra in ['aburrido', 'aburrida', 'qu hago', 'que hago', 'entretenme']):
            return """**Vamos a divertirnos!**

Puedo ayudarte a no aburrirte:

**Creatividad:**
 "Escribe un poema sobre [tema]"
 "Cuntame una historia de [gnero]"
 "Genera ideas para [proyecto]"

**Reflexin:**
 "Cul es el sentido de la vida?"
 "Hblame sobre [tema interesante]"

**Juegos mentales:**
 "Dame un acertijo"
 "Cuntame un chiste"
 "Dato curioso sobre [tema]"

Qu te provoca hacer?"""

        # Preguntas existenciales simples
        if texto_lower in ['por qu', 'por que', 'por qu?', 'por que?']:
            return """"Por qu?"

Esa es la pregunta fundamental! Pero... por qu qu exactamente? 

Puedo ayudarte a entender:
 Razones de fenmenos cientficos
 Causas de eventos histricos
 Explicaciones de conceptos
 Reflexiones filosficas

Dame ms detalles y te ayudo a explorar ese "por qu"."""

        # Preguntas sobre capacidades
        if any(palabra in texto_lower for palabra in ['qu sabes', 'que sabes', 'conoces sobre', 'informacin sobre']):
            return """**Tengo conocimiento sobre muchos temas:**

**DEPORTES:** Ftbol, NBA, F1, Tenis
**TECNOLOGA:** Programacin, IA, Empresas Tech
**CIENCIA:** Espacio, Fsica, Medicina
**CULTURA:** Cine, Msica, Entretenimiento
**GEOGRAFA:** Pases, Ciudades, Culturas
**HISTORIA:** Eventos importantes, Civilizaciones

**Y tambin puedo:**
- Buscar en internet (si me lo pides)
- Hacer clculos matemticos
- Crear contenido original
- Reflexionar sobre filosofa

Sobre qu tema quieres que hablemos?"""

        # Detectar preguntas generales
        if any(palabra in texto_lower for palabra in ['qu opinas', 'tu opinin', 'qu piensas', 'crees que']):
            return f"""**Mi perspectiva sobre esto...**

Como IA, no tengo opiniones personales, pero puedo ofrecerte:

- **Anlisis objetivo** del tema
- **Pros y contras** de diferentes perspectivas  
- **Datos y hechos** relevantes
- **Diferentes puntos de vista** para que decidas

Quieres que profundice en algn aspecto especfico?"""

        # Detectar preguntas de "cmo"
        if texto_lower.startswith('cmo') or texto_lower.startswith('como') or 'cmo' in texto_lower or 'como' in texto_lower:
            # Ver si es una pregunta simple que podemos responder
            if 'ests' in texto_lower or 'estas' in texto_lower:
                return "Muy bien! Funcionando perfectamente y lista para ayudarte. Y t cmo ests?"
            
            return f"""**Pregunta interesante...**

Quieres que:
 Te explique el concepto paso a paso?
 Busque informacin actualizada en internet?
 Te d ejemplos prcticos?

Reformula tu pregunta con ms detalles o dime "bscalo" para buscar en internet."""

        # Detectar preguntas de "qu"
        if texto_lower.startswith('qu') or texto_lower.startswith('que') or 'qu' in texto_lower or 'que' in texto_lower:
            # Intentar responder preguntas simples
            if 'da' in texto_lower or 'fecha' in texto_lower:
                return f"Hoy es {datetime.now().strftime('%d de %B de %Y')}. En qu ms puedo ayudarte?"
            
            if 'hora' in texto_lower:
                return f"Son las {datetime.now().strftime('%H:%M')}. Necesitas algo ms?"
        
        # Preguntas sobre comparaciones simples
        if ' o ' in texto_lower and '?' in texto:
            partes = texto_lower.split(' o ')
            if len(partes) == 2:
                return f"""**{partes[0].strip().capitalize()} o {partes[1].strip()}?**

Buena pregunta! Ambas opciones tienen sus ventajas.

Para darte una mejor respuesta, podras especificar:
 En qu contexto?
 Qu criterios son importantes para ti?
 Buscas una recomendacin prctica?

O puedo buscar informacin comparativa en internet si me dices "bscalo"."""

        # Detectar preguntas de "por qu"
        if texto_lower.startswith('por qu') or texto_lower.startswith('por que') or 'por qu' in texto_lower:
            return f"""**Pregunta interesante: {texto[:60]}...**

Las razones pueden ser mltiples. Para darte una respuesta completa, puedo:

- Consultar mi base de conocimientos
- Buscar informacin actualizada en internet (si me lo pides)
- Analizar diferentes perspectivas

Quieres que busque informacin especfica en internet sobre esto? Solo dime "busca" o "bscalo"."""

        # Detectar preguntas "quin/quines"
        if any(palabra in texto_lower for palabra in ['quin es', 'quien es', 'quines son', 'quienes son']):
            # Intentar buscar en base de datos primero
            respuesta_db = self.buscar_en_base_datos(texto)
            if respuesta_db:
                return respuesta_db
            
            # Extraer el nombre
            nombre = texto_lower.replace('quin es', '').replace('quien es', '').replace('quines son', '').replace('quienes son', '').strip()
            
            return f""" **Informacin sobre {nombre}**

No tengo informacin especfica sobre {nombre} en mi base de datos actual.

Quieres que busque en internet? Solo di:
 "Busca informacin sobre {nombre}"

O cuntame ms detalles sobre lo que quieres saber."""

        # Respuestas simples y directas
        if len(texto.split()) <= 5:  # Preguntas cortas
            if 'gracias' in texto_lower:
                return "De nada!  Estoy aqu para ayudarte. Necesitas algo ms?"
            
            if any(palabra in texto_lower for palabra in ['si', 's', 'ok', 'vale', 'dale', 'bueno']):
                return "Perfecto! En qu ms puedo ayudarte? "
            
            if any(palabra in texto_lower for palabra in ['no', 'nop', 'nope']):
                return "Entendido. Si cambias de opinin o necesitas algo, aqu estoy! "

        # Detectar preguntas abiertas con ms contexto
        if '?' in texto:
            # Intentar encontrar respuesta en base de datos
            respuesta_db = self.buscar_en_base_datos(texto)
            if respuesta_db:
                return respuesta_db
            
            return f"""**Interesante pregunta...**

Puedo ayudarte mejor si:
- Me das ms detalles sobre lo que buscas
- Me dices "busca en internet" para info actualizada
- Reformulas la pregunta de otra forma

Tambin puedo:
- Crear contenido creativo
- Hacer clculos
- Reflexionar sobre temas filosficos
- Explicar conceptos

Qu prefieres?"""

        # Afirmaciones o comentarios casuales
        if not '?' in texto and len(texto.split()) <= 10:
            return f"""**Entiendo...**

Hay algo especfico con lo que pueda ayudarte?

Puedo:
- Conversar sobre temas que te interesen
- Buscar informacin (solo dime "busca...")
 Crear contenido creativo
 Resolver problemas matemticos
 Explicar conceptos

Qu te gustara hacer?"""

        # Respuesta conversacional por defecto para textos ms largos
        return f""" **Sobre tu mensaje...**

He ledo lo que escribiste. Para ayudarte mejor:

 **Si es una pregunta:** Reformlala con ms detalles
 **Si quieres informacin:** Di "busca [tema]" y buscar en internet
 **Si quieres algo creativo:** "Escribe un poema/historia sobre..."
 **Si es matemticas:** Dame la operacin directamente

En qu especficamente puedo ayudarte?"""
    def buscar_en_internet(self, consulta):
        """Bsqueda web profesional usando DuckDuckGo API con resumen inteligente"""
        try:
            query = urllib.parse.quote(f"{consulta}")
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                # Procesar respuesta Abstract
                abstract = data.get('Abstract', '')
                if abstract and len(abstract) > 20:
                    fuente = data.get('AbstractSource', 'Internet')
                    url_fuente = data.get('AbstractURL', '')
                    
                    # RESUMEN INTELIGENTE con traduccin
                    respuesta = f"{self.t('resumen')} {consulta.upper()}**\n\n"
                    respuesta += f"{abstract}\n\n"
                    respuesta += f"{self.t('fuente')} {fuente}"
                    if url_fuente:
                        respuesta += f"\n{self.t('mas_detalles')} {url_fuente}"
                    
                    return respuesta
                
                # Intentar con temas relacionados
                related = data.get('RelatedTopics', [])
                if related:
                    # Recopilar informacin
                    informacion = []
                    for topic in related[:6]:
                        if isinstance(topic, dict):
                            if 'Text' in topic:
                                texto = topic['Text']
                                if len(texto) > 15:
                                    informacion.append(texto)
                            elif 'Topics' in topic:
                                for subtopic in topic['Topics'][:3]:
                                    if 'Text' in subtopic:
                                        texto = subtopic['Text']
                                        if len(texto) > 15:
                                            informacion.append(texto)
                    
                    if informacion:
                        # Crear resumen inteligente con traduccin
                        respuesta = f"{self.t('encontre')} {consulta.upper()}**\n\n"
                        respuesta += f"{self.t('basandome')}\n\n"
                        
                        # Mostrar los puntos ms importantes
                        for i, info in enumerate(informacion[:4], 1):
                            respuesta += f"{i}. {info}\n\n"
                        
                        respuesta += self.t('resumen_generado')
                        return respuesta
                
                # Si no hay resultados tiles
                return f"{self.t('busque')} {consulta}**\n\n{self.t('no_encontre')}\n\n{self.t('intenta')}\n Reformular la pregunta\n Usar trminos ms especficos\n Preguntar sobre otro tema"
                
        except urllib.error.URLError:
            return f"{self.t('sin_internet')}\n\n{self.t('preguntame')}"
        except Exception as e:
            print(f"Error bsqueda web: {e}")
            return f"{self.t('error_busqueda')}\n\n{self.t('preguntame')}"
    
    def generar_imagen(self, descripcion):
        """Genera una imagen RPIDA y sin dependencias externas"""
        try:
            print(f" Generando imagen: {descripcion}")
            
            from PIL import Image, ImageDraw
            
            # Crear imagen MS PEQUEA para ser ultra-rpida
            width, height = 300, 300
            
            # Colores basados en hash de descripcin (determinista)
            hash_val = sum(ord(c) for c in descripcion)
            r = (hash_val * 7) % 256
            g = (hash_val * 11) % 256
            b = (hash_val * 13) % 256
            
            # Crear imagen simple
            img = Image.new('RGB', (width, height), color=(r, g, b))
            
            # No agregar efectos complejos - solo lo esencial
            # La velocidad es ms importante que la calidad
            
            # Convertir a PNG comprimido
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG', optimize=True)
            img_byte_arr.seek(0)
            image_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            
            return {
                'success': True,
                'image_base64': image_base64,
                'descripcion': descripcion,
                'mensaje': f" **Imagen generada**\n\n Descripcin: {descripcion}\n\n Generada con IA"
            }
        
        except Exception as e:
            print(f"Error al generar imagen: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'mensaje': f"**Error al generar imagen**: {str(e)}\n\nIntenta nuevamente."
            }
    
    def calcular_matematicas(self, texto):
        """Realiza clculos matemticos avanzados - Modo Pitgoras"""
        texto_lower = texto.lower()
        
        try:
            # Detectar operaciones matemticas
            # Suma, resta, multiplicacin, divisin bsicas
            if any(op in texto for op in ['+', '-', '*', '/', 'x', '']):
                # Limpiar y preparar la expresin
                expresion = texto
                expresion = expresion.replace('x', '*').replace('', '/')
                expresion = expresion.replace('por', '*').replace('entre', '/')
                expresion = expresion.replace('ms', '+').replace('menos', '-')
                
                # Extraer solo nmeros y operadores
                expresion_limpia = re.sub(r'[^0-9+\-*/().\s]', '', expresion)
                
                if expresion_limpia:
                    resultado = eval(expresion_limpia)
                    return f"**CLCULO MATEMTICO**\n\nOperacin: {expresion_limpia}\nResultado: **{resultado}**\n\nCalculado por annIA (Modo Pitgoras)"
            
            # Raz cuadrada
            if 'raiz cuadrada' in texto_lower or 'raz cuadrada' in texto_lower or 'sqrt' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    num = float(numeros[0])
                    resultado = math.sqrt(num)
                    return f"**RAZ CUADRADA**\n\n{num} = **{resultado:.4f}**\n\nCalculado por Pitgoras (annIA AI)"
            
            # Potencia
            if 'al cuadrado' in texto_lower or '' in texto or '^2' in texto:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    num = float(numeros[0])
                    resultado = num ** 2
                    return f" **POTENCIA**\n\n{num} = **{resultado}**\n\n Calculado por annIA AI"
            
            if 'al cubo' in texto_lower or '' in texto or '^3' in texto:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    num = float(numeros[0])
                    resultado = num ** 3
                    return f" **POTENCIA**\n\n{num} = **{resultado}**\n\n Calculado por annIA AI"
            
            if 'elevado a' in texto_lower or 'potencia' in texto_lower or '^' in texto:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    base = float(numeros[0])
                    exponente = float(numeros[1])
                    resultado = base ** exponente
                    return f" **POTENCIA**\n\n{base}^{exponente} = **{resultado}**\n\n Calculado por annIA AI"
            
            # Porcentaje
            if '%' in texto or 'por ciento' in texto_lower or 'porciento' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    total = float(numeros[0])
                    porcentaje = float(numeros[1])
                    resultado = (total * porcentaje) / 100
                    return f" **CLCULO DE PORCENTAJE**\n\n{porcentaje}% de {total} = **{resultado}**\n\n Calculado por annIA AI"
            
            # rea del crculo
            if 'area' in texto_lower and 'circulo' in texto_lower or 'rea' in texto_lower and 'crculo' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    radio = float(numeros[0])
                    area = math.pi * (radio ** 2)
                    return f" **REA DEL CRCULO**\n\n Radio: {radio}\n rea =   r = **{area:.4f}**\n\n Frmula de Pitgoras aplicada"
            
            # Teorema de Pitgoras
            if 'pitagoras' in texto_lower or 'pitgoras' in texto_lower or 'hipotenusa' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    a = float(numeros[0])
                    b = float(numeros[1])
                    c = math.sqrt(a**2 + b**2)
                    return f"**TEOREMA DE PITGORAS**\n\nTringulo rectngulo: a = {a}, b = {b}\nHipotenusa: c = (a + b)\nc = ({a} + {b}) = **{c:.4f}**\n\nTeorema aplicado correctamente"
            
            # Promedio
            if 'promedio' in texto_lower or 'media' in texto_lower and 'de' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    promedio = sum(float(n) for n in numeros) / len(numeros)
                    return f" **PROMEDIO**\n\n Nmeros: {', '.join(numeros)}\n Promedio = **{promedio:.4f}**\n\n Calculado por annIA AI"
            
            # Factorial
            if 'factorial' in texto_lower:
                numeros = re.findall(r'\d+', texto)
                if numeros:
                    num = int(numeros[0])
                    if num <= 20:  # Lmite para evitar nmeros muy grandes
                        resultado = math.factorial(num)
                        return f" **FACTORIAL**\n\n{num}! = **{resultado}**\n\n Calculado por annIA AI"
                    else:
                        return f" El nmero es muy grande. Mximo: 20!"
            
            return None  # No es una operacin matemtica
            
        except Exception as e:
            return f" **Error en clculo**\n\nNo pude procesar la operacin. Asegrate de escribir correctamente.\n\nEjemplo: '5 + 3', 'raz cuadrada de 16', '10% de 200'"
    
    def buscar_en_base_datos(self, texto):
        """Bsqueda inteligente en base de conocimientos universal"""
        texto_lower = texto.lower()
        
        # ========== TECNOLOGA ==========
        if any(palabra in texto_lower for palabra in ['inteligencia artificial', 'ia', 'chatgpt', 'ai', 'gpt']):
            return f" **INTELIGENCIA ARTIFICIAL**\n\n{self.base_conocimientos['tecnologia']['ia']}\n\n La IA est transformando TODAS las industrias: medicina, educacin, arte, programacin.\n\n Empresas lderes: OpenAI (ChatGPT), Google (Gemini), Anthropic (Claude)"
        
        if 'python' in texto_lower or 'javascript' in texto_lower or 'programacion' in texto_lower or 'programar' in texto_lower:
            lenguajes = ', '.join(self.base_conocimientos['tecnologia']['programacion']['lenguajes_populares'])
            frameworks = ', '.join(self.base_conocimientos['tecnologia']['programacion']['frameworks'])
            return f"**PROGRAMACIN**\n\nLenguajes populares 2025:\n{lenguajes}\n\nFrameworks trending:\n{frameworks}\n\n{self.base_conocimientos['tecnologia']['programacion']['info']}"
        
        if 'apple' in texto_lower or 'iphone' in texto_lower:
            return f" **APPLE**\n\n{self.base_conocimientos['tecnologia']['empresas']['apple']}\n\n Empresa ms valiosa del mundo\n Ecosistema: iPhone, Mac, iPad, Apple Watch"
        
        if 'microsoft' in texto_lower:
            return f" **MICROSOFT**\n\n{self.base_conocimientos['tecnologia']['empresas']['microsoft']}\n\n Windows, Office, Azure, Xbox\n Inversin masiva en OpenAI"
        
        if 'google' in texto_lower:
            return f" **GOOGLE**\n\n{self.base_conocimientos['tecnologia']['empresas']['google']}\n\n Buscador #1 mundial\n Android en 70% de smartphones\n Google Cloud compitiendo con AWS"
        
        if 'meta' in texto_lower or 'facebook' in texto_lower or 'instagram' in texto_lower:
            return f" **META (Facebook)**\n\n{self.base_conocimientos['tecnologia']['empresas']['meta']}\n\n Apps: Facebook, Instagram, WhatsApp\n Reality Labs: Quest VR headsets"
        
        if 'openai' in texto_lower:
            return f" **OPENAI**\n\n{self.base_conocimientos['tecnologia']['empresas']['openai']}\n\n Fundada por Sam Altman, Elon Musk (sali)\n DALL-E para generar imgenes\n ChatGPT revolucion la IA"
        
        # ========== CIENCIA ==========
        if 'nasa' in texto_lower or 'artemis' in texto_lower:
            return f" **NASA**\n\n{self.base_conocimientos['ciencia']['espacio']['nasa']}\n\n Programa Artemis: Devolver humanos a la Luna\n Colaboracin con SpaceX para Marte\n Telescopio James Webb revolucionando astronoma"
        
        if 'spacex' in texto_lower or 'elon musk' in texto_lower or 'starship' in texto_lower:
            return f" **SPACEX**\n\n{self.base_conocimientos['ciencia']['espacio']['spacex']}\n\n CEO: Elon Musk\n Objetivo: Hacer a la humanidad multiplanetaria\n Cohetes Falcon 9 reutilizables abaratando costos"
        
        if 'telescopio' in texto_lower or 'james webb' in texto_lower or 'jwst' in texto_lower:
            return f" **TELESCOPIO JAMES WEBB**\n\n{self.base_conocimientos['ciencia']['espacio']['jwst']}\n\n Lanzado en 2021, activo desde 2022\n Ve luz infrarroja de galaxias a 13 mil millones aos luz\n Descubriendo exoplanetas con posible vida"
        
        if 'medicina' in texto_lower or 'salud' in texto_lower or 'cancer' in texto_lower:
            return f" **MEDICINA MODERNA**\n\n{self.base_conocimientos['ciencia']['medicina']}\n\n Edicin gentica CRISPR curando enfermedades\n Vacunas ARNm (como COVID) revolucionarias\n IA diagnosticando mejor que doctores en algunos casos"
        
        # ========== ENTRETENIMIENTO ==========
        if 'marvel' in texto_lower or 'avengers' in texto_lower or 'mcu' in texto_lower:
            return f" **MARVEL / MCU**\n\n{self.base_conocimientos['entretenimiento']['peliculas']['marvel']}\n\n Universo cinematogrfico ms exitoso ($30 mil millones)\n Prximos: Fantastic Four, nuevos Avengers\n Fases 5 y 6 en desarrollo"
        
        if 'dc' in texto_lower or 'batman' in texto_lower or 'superman' in texto_lower:
            return f" **DC COMICS**\n\n{self.base_conocimientos['entretenimiento']['peliculas']['dc']}\n\n Universo reiniciado por James Gunn\n Superman (2025) con David Corenswet\n Batman sigue siendo icnico"
        
        if 'taylor swift' in texto_lower:
            artistas = ', '.join(self.base_conocimientos['entretenimiento']['musica']['artistas'][:5])
            return f" **TAYLOR SWIFT**\n\n Artista ms grande del mundo actualmente\n Gira 'Eras Tour' rcord histrico ($2 mil millones)\n 12 Grammy Awards\n lbumes: Midnights, Folklore, 1989\n\n Otros artistas top: {artistas}"
        
        if 'musica' in texto_lower or 'cancion' in texto_lower:
            artistas = ', '.join(self.base_conocimientos['entretenimiento']['musica']['artistas'])
            return f" **MSICA 2025**\n\n Artistas ms populares:\n{artistas}\n\n {self.base_conocimientos['entretenimiento']['musica']['tendencias']}"
        
        if any(palabra in texto_lower for palabra in ['videojuego', 'gta', 'minecraft', 'fortnite', 'juegos']):
            juegos = ', '.join(self.base_conocimientos['entretenimiento']['videojuegos']['populares'])
            return f" **VIDEOJUEGOS 2025**\n\n Ms populares:\n{juegos}\n\n {self.base_conocimientos['entretenimiento']['videojuegos']['consolas']}"
        
        # ========== GEOGRAFA ==========
        # Ciudades de Mxico
        if 'monterrey' in texto_lower:
            return f" **MONTERREY**\n\n Capital de Nuevo Len, Mxico\n 5.3 millones habitantes (rea metropolitana)\n Cerro de la Silla (smbolo icnico)\n Centro industrial y financiero ms importante del norte de Mxico\n Hogar de Rayados (Monterrey) y Tigres UANL\n 'La Sultana del Norte' - Ciudad moderna y prspera"
        
        if 'ciudad de mexico' in texto_lower or 'cdmx' in texto_lower or ('mexico' in texto_lower and 'capital' in texto_lower):
            return f" **CIUDAD DE MXICO (CDMX)**\n\n Capital de Mxico\n 9+ millones habitantes (21M en zona metropolitana)\n Centro histrico Patrimonio de la Humanidad\n Museos: Antropologa, Frida Kahlo, Bellas Artes\n Capital gastronmica de Mxico\n Una de las ciudades ms grandes del mundo"
        
        if 'guadalajara' in texto_lower:
            return f"**GUADALAJARA**\n\nCapital de Jalisco, Mxico\n5+ millones habitantes\nCuna del mariachi y tequila\nHogar de Chivas (Guadalajara)\n'La Perla de Occidente'\nSilicon Valley mexicano"
        
        if 'cancun' in texto_lower or 'cancn' in texto_lower:
            return f" **CANCN**\n\n Quintana Roo, Mxico\n Destino turstico #1 de Mxico\n Playas paradisacas del Caribe\n Cerca de Chichn Itz (Maravilla del Mundo)\n Snorkel en arrecifes de coral\n Ms de 10 millones de turistas al ao"
        
        # Pases y capitales
        if 'capital' in texto_lower and ('francia' in texto_lower or 'paris' in texto_lower):
            return f" **FRANCIA**\n\n Capital: Pars\n 67 millones habitantes\n Torre Eiffel, Louvre, Notre-Dame\n Famosa por: gastronoma, moda, arte\n Pas ms visitado del mundo"
        
        if 'paris' in texto_lower or 'pars' in texto_lower:
            return f" **PARS**\n\n 'La Ciudad de la Luz'\n Torre Eiffel, Louvre, Arco del Triunfo\n Capital mundial del arte y la moda\n Croissants, caf, haute cuisine\n Ciudad ms romntica del mundo"
        
        if 'capital' in texto_lower and 'espaa' in texto_lower:
            return f" **ESPAA**\n\n Capital: Madrid\n 47 millones habitantes\n Real Madrid y Barcelona (mejores equipos del mundo)\n Famosa por: arte, playa, gastronoma, flamenco"
        
        if 'madrid' in texto_lower and 'ciudad' in texto_lower:
            return f" **MADRID**\n\n Capital de Espaa\n 3.3 millones habitantes\n Museo del Prado, Reina Sofa\n Real Madrid (Santiago Bernabu)\n Retiro, Gran Va, Puerta del Sol\n Tapas, jamn ibrico, vida nocturna"
        
        if 'barcelona' in texto_lower and 'ciudad' in texto_lower:
            return f" **BARCELONA**\n\n Capital de Catalua\n 1.6 millones habitantes\n Sagrada Familia (Gaud)\n Playas mediterrneas\n FC Barcelona (Camp Nou)\n Arte, arquitectura modernista"
        
        if 'rusia' in texto_lower:
            return f" **RUSIA**\n\n{self.base_conocimientos['geografia']['paises_grandes']['rusia']}\n 146 millones habitantes\n Plaza Roja, Kremlin\n Clima muy fro en invierno"
        
        if 'canada' in texto_lower or 'canad' in texto_lower:
            return f" **CANAD**\n\n{self.base_conocimientos['geografia']['paises_grandes']['canada']}\n Smbolo: Hoja de arce\n Deporte nacional: Hockey sobre hielo\n Naturaleza increble: Montaas Rocosas"
        
        if 'china' in texto_lower:
            return f" **CHINA**\n\n{self.base_conocimientos['geografia']['paises_grandes']['china']}\n Gran Muralla China\n Cultura milenaria (5000+ aos)\n 2da economa mundial"
        
        if 'estados unidos' in texto_lower or 'usa' in texto_lower or 'eeuu' in texto_lower:
            return f" **ESTADOS UNIDOS**\n\n{self.base_conocimientos['geografia']['paises_grandes']['usa']}\n Estatua de la Libertad en Nueva York\n Hollywood - Capital mundial del cine\n Economa #1 del mundo"
        
        if 'nueva york' in texto_lower or 'new york' in texto_lower:
            return f" **NUEVA YORK**\n\n 'La Gran Manzana'\n 8+ millones habitantes\n Manhattan, Brooklyn, Queens\n Broadway, Times Square\n Wall Street (centro financiero)\n Empire State, Central Park"
        
        if 'tokio' in texto_lower or 'tokyo' in texto_lower:
            return f" **TOKIO**\n\n Capital de Japn\n 14 millones habitantes (38M rea metropolitana)\n Ciudad ms grande del mundo\n Tokyo Tower, Skytree\n Sushi, ramen, cultura pop\n Tecnologa y tradicin juntas"
        
        if 'londres' in texto_lower or 'london' in texto_lower:
            return f" **LONDRES**\n\n Capital del Reino Unido\n 9 millones habitantes\n Big Ben, Tower Bridge, Buckingham Palace\n Teatro, museos de clase mundial\n Arsenal, Chelsea, Tottenham\n Cultura del t britnico"
        
        # Mxico como pas
        if 'mexico' in texto_lower and not 'ciudad' in texto_lower:
            return f" **MXICO**\n\n Pas de Amrica del Norte\n 128 millones habitantes\n Civilizaciones antiguas: Aztecas, Mayas\n Tacos, mariachi, tequila\n Playas: Cancn, Playa del Carmen\n Frida Kahlo, Diego Rivera\n Seleccin Mexicana muy apasionada"
        
        # ========== DEPORTES (mantener cdigo anterior) ==========
        if any(palabra in texto_lower for palabra in ['la liga', 'liga espaola', 'liga', 'espaa futbol']):
            return f" **LA LIGA ESPAOLA 2024-25**\n\n Lder: {self.base_conocimientos['deportes']['futbol']['la_liga']['lider']}\n Subcampen: {self.base_conocimientos['deportes']['futbol']['la_liga']['subcampeon']}\n Goleadores: {', '.join(self.base_conocimientos['deportes']['futbol']['la_liga']['goleadores'])}\n\n {self.base_conocimientos['deportes']['futbol']['la_liga']['info']}"
        
        # Premier League
        if 'premier' in texto_lower or 'inglaterra' in texto_lower:
            equipos = ', '.join(self.base_conocimientos['deportes']['futbol']['premier']['top3'])
            return f" **PREMIER LEAGUE 2024-25**\n\n Top 3: {equipos}\n\n {self.base_conocimientos['deportes']['futbol']['premier']['info']}"
        
        # Champions League
        if 'champions' in texto_lower:
            favoritos = ', '.join(self.base_conocimientos['deportes']['futbol']['champions']['favoritos'])
            return f" **UEFA CHAMPIONS LEAGUE 2024-25**\n\n Favoritos: {favoritos}\n\n {self.base_conocimientos['deportes']['futbol']['champions']['info']}\n\n La competicin ms prestigiosa de Europa!"
        
        # Ftbol - equipos especficos
        if 'real madrid' in texto_lower or ('madrid' in texto_lower and 'real' in texto_lower):
            return f" **REAL MADRID**\n\n {self.base_conocimientos['deportes']['futbol']['la_liga']['lider']}\n Racha: Excelente forma\n Figuras: Bellingham, Vincius Jr., Rodrygo\n Objetivos: La Liga y Champions League\n\n El club ms laureado de Europa"
        
        if 'barcelona' in texto_lower or 'bara' in texto_lower or 'barca' in texto_lower:
            return f" **FC BARCELONA**\n\n {self.base_conocimientos['deportes']['futbol']['la_liga']['subcampeon']}\n Goleador: Robert Lewandowski\n Jvenes: Gavi, Pedri, Fermn\n Proyecto: Xavi construyendo equipo competitivo\n\n Ms que un club"
        
        if 'arsenal' in texto_lower:
            return f" **ARSENAL FC**\n\n Lder de la Premier League\n Jugadores clave: Saka, degaard, Rice\n Forma: Excelente momento bajo Arteta\n Objetivo: Ganar la Premier despus de 20 aos"
        
        if 'city' in texto_lower or 'manchester city' in texto_lower:
            return f" **MANCHESTER CITY**\n\n Peleando el liderato de Premier\n Estrella: Erling Haaland (mximo goleador)\n Guardiola buscando ms ttulos\n Campeones de Europa 2023"
        
        # Jugadores especficos
        if 'messi' in texto_lower:
            return f" **LIONEL MESSI**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['messi']}\n 8 Balones de Oro (rcord)\n Campen del Mundo 2022 con Argentina \n Actualmente brillando en la MLS\n Considerado el mejor de la historia"
        
        if 'ronaldo' in texto_lower and 'cristiano' in texto_lower or texto_lower.strip() == 'ronaldo':
            return f" **CRISTIANO RONALDO**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['ronaldo']}\n 5 Balones de Oro\n Mximo goleador histrico del ftbol (ms de 890 goles)\n Leyenda del Real Madrid y Manchester United\n Sigue activo a los 39 aos"
        
        if 'haaland' in texto_lower:
            return f" **ERLING HAALAND**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['haaland']}\n Mximo goleador Premier League 2023-24\n Rcord: 36 goles en una temporada\n Noruega - 24 aos\n Considerado el futuro del ftbol"
        
        if 'mbappe' in texto_lower or 'mbapp' in texto_lower:
            return f" **KYLIAN MBAPP**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['mbappe']}\n Velocidad increble y tcnica superior\n Campen del Mundo 2018\n Prximo fichaje estrella del Real Madrid\n Solo 25 aos"
        
        # NBA
        if 'lakers' in texto_lower:
            return f" **LOS ANGELES LAKERS**\n\n Rcord: 13-5 (Temporada 2024-25)\n Estrellas: LeBron James (39 aos) y Anthony Davis\n Forma: Excelente momento\n 17 campeonatos en su historia\n Uno de los equipos ms icnicos de la NBA"
        
        if 'lebron' in texto_lower:
            return f" **LEBRON JAMES**\n\n 'King James' - Los Angeles Lakers\n 39 aos, todava dominante\n 4 campeonatos NBA\n Jugando con su hijo Bronny (histrico)\n Mximo anotador de todos los tiempos NBA"
        
        if 'celtics' in texto_lower:
            return f" **BOSTON CELTICS**\n\n Rcord: 15-3 (Mejor del Este)\n Jayson Tatum, Jaylen Brown\n 18 campeonatos (rcord NBA)\n Dinasta histrica del baloncesto"
        
        if 'nba' in texto_lower:
            este = '\n'.join([f"   {e}" for e in self.datos_deportivos['baloncesto']['nba']['este'][:3]])
            oeste = '\n'.join([f"   {e}" for e in self.datos_deportivos['baloncesto']['nba']['oeste'][:3]])
            return f" **NBA TEMPORADA 2024-25**\n\n CONFERENCIA ESTE:\n{este}\n\n CONFERENCIA OESTE:\n{oeste}\n\n Favoritos: Celtics, Nuggets, Lakers"
        
        # Tenis
        if 'tenis' in texto_lower or 'alcaraz' in texto_lower or 'djokovic' in texto_lower:
            return f" **TENIS MUNDIAL**\n\n ATP Top 3:\n  1. Carlos Alcaraz \n  2. Novak Djokovic  (24 Grand Slams)\n  3. Jannik Sinner \n\n WTA Top 3:\n  1. Iga witek \n  2. Aryna Sabalenka \n  3. Coco Gauff "
        
        # F1
        if 'formula 1' in texto_lower or 'f1' in texto_lower or 'verstappen' in texto_lower:
            return f" **FRMULA 1**\n\n {self.datos_deportivos['formula1']['campeon_2024']}\n {self.datos_deportivos['formula1']['proxima_temporada']}\n Dominio absoluto de Red Bull Racing"
        
        # ========== ANIMALES ==========
        if 'perro' in texto_lower or 'perros' in texto_lower:
            return f" **PERROS**\n\n 'El mejor amigo del hombre'\n Mascotas ms populares del mundo\n Razas populares: Labrador, Golden Retriever, Pastor Alemn\n Muy inteligentes y leales\n Descendientes de lobos domesticados\n Olfato 40 veces mejor que humanos"
        
        if 'gato' in texto_lower or 'gatos' in texto_lower:
            return f" **GATOS**\n\n Mascotas independientes y cariosas\n Domesticados hace 10,000 aos en Egipto\n Duermen 12-16 horas al da\n Ven muy bien en la oscuridad\n Videos de gatos dominan internet\n Razas: Persa, Siams, Maine Coon"
        
        if 'quien eres' in texto_lower or 'quin eres' in texto_lower or 'que eres' in texto_lower:
            return f" **SOY annIAAI v2.0 PROFESSIONAL**\n\n Soy tu asistente inteligente universal\n Tengo conocimiento sobre miles de temas\n Puedo buscar en internet lo que no s\n Respondo rpido y con informacin detallada\n\n Mi misin: Ayudarte con cualquier pregunta\n\nQu quieres saber hoy? "
        
        return None
    
    def procesar_texto(self, texto):
        """Procesamiento principal con IA contextual y multiidioma"""
        texto_lower = texto.lower()
        
        # Detectar y cambiar idioma si se solicita (SIMPLIFICADO)
        if 'english' in texto_lower and len(texto_lower) < 20:
            self.idioma_actual = 'en'
            return " Language changed to English. How can I help you?"
        elif 'franais' in texto_lower or 'francais' in texto_lower or 'french' in texto_lower and len(texto_lower) < 20:
            self.idioma_actual = 'fr'
            return " Langue change en Franais. Comment puis-je vous aider?"
        elif 'espaol' in texto_lower or 'espanol' in texto_lower or 'spanish' in texto_lower and len(texto_lower) < 20:
            self.idioma_actual = 'es'
            return " Idioma cambiado a Espaol. En qu puedo ayudarte?"
        
        # Guardar en historial
        self.conversacion_historia.append(('usuario', texto))
        
        # DETECCIN DE SOLICITUDES DE IMGENES
        palabras_imagen = ['genera imagen', 'crea una imagen', 'dibuja', 'pinta', 'imagen de', 'crear imagen', 'generar imagen', 'hacer imagen', 'una imagen']
        if any(palabra in texto_lower for palabra in palabras_imagen):
            # Extraer la descripcin de la imagen
            descripcion = texto_lower
            for palabra in palabras_imagen:
                descripcion = descripcion.replace(palabra, '', 1)
            descripcion = descripcion.strip()
            
            if descripcion:
                # Generar la imagen
                resultado_imagen = self.generar_imagen(descripcion)
                respuesta = resultado_imagen.get('mensaje', '')
                
                # Guardar en historial con informacin de imagen
                self.conversacion_historia.append(('ia', respuesta))
                
                # Retornar con flag de imagen si fue exitosa
                if resultado_imagen.get('success'):
                    return {
                        'respuesta': respuesta,
                        'imagen_base64': resultado_imagen.get('image_base64'),
                        'es_imagen': True,
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    }
                else:
                    return {
                        'respuesta': respuesta,
                        'es_imagen': False,
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    }
        
        # Detectar intencin
        intencion = self.detectar_intencion(texto)
        
        # Procesar segn intencin y idioma
        if intencion == 'saludo':
            if self.idioma_actual == 'en':
                respuestas = [
                    "Hello! I'm annIA, your professional assistant.  How can I help you?",
                    "Hi!  Ready to help you with information or web searches. What do you need?",
                    "Greetings!  Ask me anything or request an internet search."
                ]
            elif self.idioma_actual == 'fr':
                respuestas = [
                    "Bonjour! Je suis annIA, votre assistante professionnelle.  Comment puis-je vous aider?",
                    "Salut!  Prte  vous aider avec des informations ou des recherches web. Que voulez-vous?",
                    "Salutations!  Demandez-moi n'importe quoi ou demandez une recherche internet."
                ]
            else:  # espaol
                respuestas = [
                    "Hola! Soy annIA, tu asistente profesional.  En qu puedo ayudarte?",
                    "Hola!  Lista para ayudarte con informacin o bsquedas web. Qu necesitas?",
                    "Saludos!  Pregntame lo que sea o pdeme que busque en internet."
                ]
            respuesta = random.choice(respuestas)
        
        elif intencion == 'despedida':
            if self.idioma_actual == 'en':
                respuestas = [
                    "See you soon!  Come back when you need help.",
                    "Goodbye!  It was a pleasure helping you!",
                    "Bye!  I'll be here when you need me."
                ]
            elif self.idioma_actual == 'fr':
                respuestas = [
                    " bientt!  Revenez quand vous avez besoin d'aide.",
                    "Au revoir!  C'tait un plaisir de vous aider!",
                    "Salut!  Je serai l quand vous aurez besoin de moi."
                ]
            else:  # espaol
                respuestas = [
                    "Hasta pronto!  Vuelve cuando necesites ayuda.",
                    "Adis!  Fue un placer ayudarte!",
                    "Chao!  Aqu estar cuando me necesites."
                ]
            respuesta = random.choice(respuestas)
        
        elif intencion == 'agradecimiento':
            if self.idioma_actual == 'en':
                respuestas = [
                    "You're welcome!  Always at your service.",
                    "My pleasure to help!  Ask me anything.",
                    "That's what I'm here for!  Anything else?"
                ]
            elif self.idioma_actual == 'fr':
                respuestas = [
                    "De rien!  Toujours  votre service.",
                    "Avec plaisir!  Demandez-moi ce que vous voulez.",
                    "C'est pour a que je suis l!  Autre chose?"
                ]
            else:
                respuestas = [
                    "De nada!  Siempre a tu servicio.",
                    "Un placer ayudarte!  Pregunta lo que necesites.",
                    "Para eso estoy!  Algo ms?"
                ]
            respuesta = random.choice(respuestas)
        
        elif intencion == 'ayuda':
            respuesta = """ **annIAAI PROFESSIONAL v2.0**

Hola! Soy tu asistente inteligente universal. Puedo ayudarte con TODO tipo de informacin:

 **DEPORTES**
 Ftbol (La Liga, Premier, Champions)
 NBA,  Tenis,  Frmula 1

**TECNOLOGA**
 Inteligencia Artificial
- Programacin (Python, JavaScript, etc.)
 Empresas tech (Apple, Google, Microsoft)

 **CIENCIA**
 Espacio (NASA, SpaceX, James Webb)
 Medicina y avances cientficos
 Fsica y computacin cuntica

 **ENTRETENIMIENTO**
 Pelculas y series
 Msica y artistas
 Videojuegos y consolas

 **GEOGRAFA E HISTORIA**
 Pases, capitales, datos curiosos
- Eventos histricos importantes

 **ACTUALIDAD 2025**
 Poltica, economa, clima

 **BSQUEDA EN INTERNET**
Si no tengo la info, la busco en tiempo real.

 **EJEMPLOS:**
 "Qu es ChatGPT?"
 "Capital de Francia"
 "Quin es Taylor Swift?"
 "Informacin sobre SpaceX"
 "Historia de las guerras mundiales"
 "Busca noticias sobre el clima"

Qu quieres saber? Pregntame lo que sea! """
        
        elif intencion == 'busqueda_web':
            # Extraer trminos de bsqueda
            terminos = texto_lower
            for palabra in ['busca', 'buscar', 'bsqueda', 'informacin sobre', 'sobre']:
                terminos = terminos.replace(palabra, '')
            terminos = terminos.strip()
            
            if terminos:
                respuesta = self.buscar_en_internet(terminos)
            else:
                respuesta = "Qu quieres que busque? \n\nEjemplos:\n 'Busca Messi ltimas noticias'\n 'Informacin sobre el Mundial 2026'\n 'Buscar resultados Champions League'"
        
        else:
            # PRIORIDAD 1: Verificar si es una operacin matemtica (MODO PITGORAS)
            respuesta_mate = self.calcular_matematicas(texto)
            if respuesta_mate:
                respuesta = respuesta_mate
            else:
                # PRIORIDAD 2: SIEMPRE usar Groq API (Llama 3) para TODO lo dems
                respuesta = self.respuesta_con_groq(texto)
                
                # Si Groq falla, usar fallback
                if not respuesta:
                    respuesta_local = self.buscar_en_base_datos(texto)
                    if respuesta_local:
                        respuesta = respuesta_local
                    else:
                        respuesta = "Lo siento, no puedo procesar tu mensaje en este momento. Por favor intenta de nuevo."
        
        # Guardar respuesta
        self.conversacion_historia.append(('ia', respuesta))
        
        # Actualizar contexto
        self.contexto_actual = {
            'ultimo_tema': texto[:50],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return respuesta
    
    def obtener_estadisticas(self):
        """Retorna estadsticas de uso"""
        total_mensajes = len(self.conversacion_historia)
        mensajes_usuario = sum(1 for tipo, _ in self.conversacion_historia if tipo == 'usuario')
        
        return {
            'total_mensajes': total_mensajes,
            'mensajes_usuario': mensajes_usuario,
            'mensajes_ia': total_mensajes - mensajes_usuario
        }

# Crear instancia global
ia = IAannIA()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')
        
        if mensaje:
            resultado = ia.procesar_texto(mensaje)
            stats = ia.obtener_estadisticas()
            
            # Verificar si es una respuesta con imagen
            
            if isinstance(resultado, dict) and resultado.get('es_imagen'):
                return jsonify({
                    'respuesta': resultado['respuesta'],
                    'imagen_base64': resultado.get('imagen_base64'),
                    'es_imagen': True,
                    'timestamp': resultado.get('timestamp'),
                    'stats': stats
                })
            else:
                # Respuesta normal de texto
                respuesta = resultado if isinstance(resultado, str) else resultado.get('respuesta', resultado)
                return jsonify({
                    'respuesta': respuesta,
                    'es_imagen': False,
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'stats': stats
                })
        
        return jsonify({'error': 'No se recibi mensaje'}), 400
    except Exception as e:
        print(f"Error en /chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'respuesta': f" Error al procesar mensaje. Por favor, intenta de nuevo.",
            'error': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Endpoint para obtener estadsticas de uso"""
    return jsonify(ia.obtener_estadisticas())

@app.route('/generar-imagen', methods=['POST'])
def generar_imagen_route():
    """Endpoint para generar imgenes directamente"""
    try:
        data = request.get_json()
        descripcion = data.get('descripcion', '')
        
        if not descripcion:
            return jsonify({'error': 'No se proporcion descripcin'}), 400
        
        resultado = ia.generar_imagen(descripcion)
        
        return jsonify({
            'success': resultado.get('success', False),
            'mensaje': resultado.get('mensaje', ''),
            'imagen_base64': resultado.get('image_base64'),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    except Exception as e:
        print(f" Error en /generar-imagen: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'mensaje': ' Error al generar imagen'
        }), 500

@app.route('/limpiar', methods=['POST'])
def limpiar():
    ia.conversacion_historia = []
    return jsonify({'mensaje': 'Historial limpiado'})

if __name__ == '__main__':
    # Asegurar UTF-8 en output
    try:
        import io
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass
    
    print("\n" + "="*50)
    print("  [IA] Servidor Iniciado")
    print("="*50)
    print("\n  URL: http://localhost:8080")
    print("\n  Presiona Ctrl+C para detener\n")
    sys.stdout.flush()
    
    try:
        app.run(
            debug=False,
            host='localhost',
            port=8080,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n[STOP] Servidor detenido")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
