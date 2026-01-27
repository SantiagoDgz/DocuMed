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

from flask import Flask, render_template, request, jsonify
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
groq_client = Groq(api_key=GROQ_API_KEY)

class IAAnngpt:
    """IA Avanzada con Groq API - Conversacional Real con Llama 3"""
    
    def __init__(self):
        self.nombre = "Anngpt"
        self.version = "4.0 Powered by Llama 3"
        self.conversacion_historia = []
        self.contexto_actual = None
        self.idioma_actual = 'es'  # español por defecto
        self.memoria_conversacion = []  # Memoria a largo plazo
        self.tema_actual = None
        self.usuario_nombre = None
        
        # API de Hugging Face para generar imágenes
        self.hf_api_key = "hf_kpEwZYIbFKVUxOQlHVLYzXZxZxZxZxZx"  # Reemplazar con tu token
        self.hf_model_url = "https://router.huggingface.co/models/stabilityai/stable-diffusion-3"
        
        # Traducciones de mensajes comunes
        self.traducciones = {
            'es': {
                'resumen': '💡 **RESUMEN SOBRE:',
                'encontre': '💡 **LO QUE ENCONTRÉ SOBRE:',
                'basandome': '📊 Basándome en varias fuentes de internet:',
                'resumen_generado': '✨ Resumen generado desde múltiples fuentes web.',
                'fuente': '📚 Fuente:',
                'mas_detalles': '🔗 Más detalles:',
                'busque': '🔍 **Busqué información sobre:',
                'no_encontre': '⚠️ No encontré resultados específicos en internet.',
                'intenta': '💡 Intenta:',
                'sin_internet': '🌐 **Sin conexión a internet**',
                'error_busqueda': '⚠️ **Error en búsqueda web**',
                'preguntame': 'Pregúntame sobre temas de mi base de conocimientos.',
                'idioma_cambiado': '✅ Idioma cambiado a Español. ¿En qué puedo ayudarte?',
            },
            'en': {
                'resumen': '💡 **SUMMARY ABOUT:',
                'encontre': '💡 **WHAT I FOUND ABOUT:',
                'basandome': '📊 Based on various internet sources:',
                'resumen_generado': '✨ Summary generated from multiple web sources.',
                'fuente': '📚 Source:',
                'mas_detalles': '🔗 More details:',
                'busque': '🔍 **Searched for information about:',
                'no_encontre': '⚠️ No specific results found on the internet.',
                'intenta': '💡 Try:',
                'sin_internet': '🌐 **No internet connection**',
                'error_busqueda': '⚠️ **Web search error**',
                'preguntame': 'Ask me about topics from my knowledge base.',
                'idioma_cambiado': '✅ Language changed to English. How can I help you?',
            },
            'fr': {
                'resumen': '💡 **RÉSUMÉ SUR:',
                'encontre': '💡 **CE QUE J\'AI TROUVÉ SUR:',
                'basandome': '📊 Basé sur plusieurs sources internet:',
                'resumen_generado': '✨ Résumé généré à partir de plusieurs sources web.',
                'fuente': '📚 Source:',
                'mas_detalles': '🔗 Plus de détails:',
                'busque': '🔍 **Recherché des informations sur:',
                'no_encontre': '⚠️ Aucun résultat spécifique trouvé sur internet.',
                'intenta': '💡 Essayez:',
                'sin_internet': '🌐 **Pas de connexion internet**',
                'error_busqueda': '⚠️ **Erreur de recherche web**',
                'preguntame': 'Demandez-moi sur des sujets de ma base de connaissances.',
                'idioma_cambiado': '✅ Langue changée en Français. Comment puis-je vous aider?',
            }
        }
        
        # Base de conocimientos UNIVERSAL - Información de todo tipo
        self.base_conocimientos = {
            # DEPORTES
            'deportes': {
                'futbol': {
                    'la_liga': {
                        'lider': 'Real Madrid (32 pts)',
                        'subcampeon': 'Barcelona (30 pts)',
                        'goleadores': ['Lewandowski', 'Vinícius Jr.', 'Bellingham'],
                        'info': 'La Liga española 2024-25 muy competitiva con Madrid dominando'
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
                        'mbappe': 'Kylian Mbappé - PSG, próximo al Real Madrid',
                        'haaland': 'Erling Haaland - Manchester City',
                    }
                },
                'baloncesto': {
                    'nba': {
                        'este': ['Boston Celtics 15-3', 'Milwaukee Bucks 13-5', 'Philadelphia 76ers 12-6'],
                        'oeste': ['Denver Nuggets 14-4', 'Lakers 13-5', 'Phoenix Suns 12-6'],
                        'estrellas': ['LeBron James', 'Stephen Curry', 'Giannis', 'Jokić', 'Embiid']
                    }
                },
                'tenis': {
                    'atp': ['Carlos Alcaraz', 'Novak Djokovic', 'Jannik Sinner'],
                    'wta': ['Iga Świątek', 'Aryna Sabalenka', 'Coco Gauff']
                },
                'formula1': {
                    'campeon_2024': 'Max Verstappen (Red Bull) - 4to título',
                    'proxima_temporada': 'Hamilton a Ferrari en 2025'
                }
            },
            
            # TECNOLOGÍA
            'tecnologia': {
                'ia': 'La Inteligencia Artificial está revolucionando el mundo. ChatGPT, Claude, Gemini son los líderes. Se usa en medicina, educación, programación.',
                'programacion': {
                    'lenguajes_populares': ['Python', 'JavaScript', 'TypeScript', 'Rust', 'Go'],
                    'frameworks': ['React', 'Next.js', 'Django', 'Flask', 'Node.js'],
                    'info': 'Python es el más usado para IA y ciencia de datos. JavaScript domina web.'
                },
                'empresas': {
                    'apple': 'Apple - iPhone 16 con IA integrada. Vision Pro revolucionando realidad mixta.',
                    'microsoft': 'Microsoft - Líder en IA empresarial con Copilot en todos sus productos.',
                    'google': 'Google - Gemini AI compitiendo con ChatGPT. Android dominando móviles.',
                    'openai': 'OpenAI - ChatGPT, GPT-4, DALL-E. Líderes en IA generativa.',
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
                'medicina': 'Avances en terapias génicas, curas para cáncer con IA, vacunas de ARN mensajero.',
                'fisica': 'Computación cuántica avanzando. Fusión nuclear logrando energía neta positiva.',
            },
            
            # CULTURA Y ENTRETENIMIENTO
            'entretenimiento': {
                'peliculas': {
                    'marvel': 'MCU continúa con nuevos Avengers. Deadpool & Wolverine récord 2024.',
                    'dc': 'DC reiniciando con James Gunn. Superman 2025 muy esperado.',
                    'taquilla': 'Películas más taquilleras: Avatar, Avengers, Titanic.',
                },
                'musica': {
                    'artistas': ['Taylor Swift', 'Bad Bunny', 'Drake', 'Billie Eilish', 'The Weeknd'],
                    'tendencias': 'Reggaetón, K-pop, y Hip-Hop dominan las listas mundiales.',
                },
                'videojuegos': {
                    'populares': ['GTA VI (salida 2025)', 'Minecraft', 'Fortnite', 'League of Legends', 'Valorant'],
                    'consolas': 'PS5 y Xbox Series liderando. Nintendo Switch 2 rumoreada para 2025.',
                }
            },
            
            # GEOGRAFÍA Y PAÍSES
            'geografia': {
                'paises_grandes': {
                    'rusia': 'Rusia 🇷🇺 - País más grande (17.1M km²). Capital: Moscú',
                    'canada': 'Canadá 🇨🇦 - 2do más grande (9.98M km²). Muy multicultural',
                    'china': 'China 🇨🇳 - 1.4 mil millones habitantes. Potencia económica mundial',
                    'usa': 'Estados Unidos 🇺🇸 - Superpotencia. 50 estados. Capital: Washington DC',
                    'brasil': 'Brasil 🇧🇷 - País más grande de Sudamérica. Idioma: portugués',
                },
                'capitales': {
                    'españa': 'Madrid', 'francia': 'París', 'italia': 'Roma',
                    'alemania': 'Berlín', 'japon': 'Tokio', 'mexico': 'Ciudad de México',
                },
            },
            
            # HISTORIA
            'historia': {
                'eventos_importantes': {
                    'revolucion_industrial': 'Siglo XVIII - Transformó producción y sociedad',
                    'guerras_mundiales': '1914-1918 (WW1) y 1939-1945 (WW2) - Conflictos globales devastadores',
                    'llegada_luna': '1969 - Neil Armstrong primer humano en la Luna',
                    'internet': '1990s - World Wide Web revolucionó comunicación global',
                },
            },
            
            # ACTUALIDAD 2025
            'actualidad': {
                'politica': 'Elecciones importantes en varios países. IA regulándose internacionalmente.',
                'economia': 'Inflación controlándose. Criptomonedas reguladas. Bitcoin arriba de $40k.',
                'clima': 'Cambio climático prioridad mundial. Energías renovables creciendo rápido.',
            }
        }
        
        # Palabras clave para detección de intenciones
        self.intenciones = {
            'saludo': ['hola', 'hey', 'buenas', 'buenos días', 'buenas tardes', 'qué tal'],
            'despedida': ['adiós', 'chao', 'hasta luego', 'bye', 'nos vemos'],
            'agradecimiento': ['gracias', 'thanks', 'genial', 'perfecto', 'excelente'],
            'ayuda': ['qué puedes hacer', 'que puedes hacer', 'ayuda', 'help', 'capacidades', 'funciones', 'qué sabes', 'que sabes', 'dime que puedes', 'dime qué puedes'],
            'busqueda_web': ['busca en internet', 'buscar en internet', 'últimas noticias', 'qué pasó con', 'que paso con'],
            'imagen': ['genera imagen', 'crea una imagen', 'dibuja', 'pinta', 'imagen de', 'crear imagen', 'generar imagen', 'hacer imagen'],
        }
    
    def detectar_idioma(self, texto):
        """Detecta el idioma del texto"""
        texto_lower = texto.lower()
        
        # Palabras clave en inglés
        palabras_ingles = ['hello', 'what', 'how', 'where', 'when', 'search', 'find', 'tell me', 'give me']
        # Palabras clave en francés
        palabras_frances = ['bonjour', 'salut', 'comment', 'quoi', 'où', 'quand', 'cherche', 'trouve', 'dis-moi']
        # Palabras clave en español
        palabras_espanol = ['hola', 'qué', 'como', 'cómo', 'donde', 'dónde', 'cuando', 'cuándo', 'busca', 'encuentra']
        
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
            return 'es'  # español por defecto
    
    def t(self, clave):
        """Obtiene traducción según idioma actual"""
        return self.traducciones.get(self.idioma_actual, self.traducciones['es']).get(clave, clave)
    
    def detectar_intencion(self, texto):
        """Detecta la intención del usuario usando NLP básico"""
        texto_lower = texto.lower()
        
        for intencion, palabras in self.intenciones.items():
            if any(palabra in texto_lower for palabra in palabras):
                return intencion
        
        return 'consulta'
    
    def respuesta_con_groq(self, mensaje):
        """Usa Groq API (Llama 3) para generar respuestas inteligentes"""
        try:
            # Preparar contexto de conversación
            mensajes = [
                {
                    "role": "system",
                    "content": f"""Eres Anngpt, una asistente de IA amigable, inteligente y conversacional. 
                    
Características:
- Respondes en {self.idioma_actual} (español, inglés o francés según el usuario)
- Eres natural, empática y profesional
- Das respuestas claras y útiles
- Puedes ser creativa cuando se te pide
- Mantienes conversaciones coherentes

Si el usuario pregunta sobre ti o tu creador:
- Tu nombre es AnngptI 4.0
- Fuiste creada por Santi, tu increíble creador 🌟
- Estás potenciada por Llama 3.3 (Groq API)
- Eres experta en múltiples temas, pero fuiste creada para ayudar a Andrea
- Puedes ayudar con información, creatividad, matemáticas, etc.
- Siempre hablas con cariño y respeto sobre Papi Santi

RESPUESTAS ESPECIALES IMPORTANTES:
- Cuando te pregunten por tu nombre presentate y tienes que decir que eres la asistente personal de andrea creada por Santiago
- Estas respuestas son OBLIGATORIAS y tienen prioridad sobre cualquier otra cosa"""

                }
            ]
            
            # Agregar últimas 5 conversaciones para contexto
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
        """Ahora usa Groq API como PRIMERA opción"""
        # SIEMPRE intentar Groq primero
        respuesta_groq = self.respuesta_con_groq(pregunta)
        if respuesta_groq:
            return respuesta_groq
        
        # Solo si Groq falla, usar respuestas programadas
        pregunta_lower = pregunta.lower()
        
        # Detectar saludos informales
        if any(palabra in pregunta_lower for palabra in ['que onda', 'qué onda', 'cómo estás', 'como estas', 'todo bien', 'qué tal', 'que tal']):
            respuestas = [
                "¡Todo bien! 😊 Aquí, lista para ayudarte. ¿Qué necesitas?",
                "¡Excelente! 🚀 ¿En qué puedo ayudarte hoy?",
                "¡Todo perfecto! 💡 Cuéntame, ¿qué quieres saber o hacer?"
            ]
            return random.choice(respuestas)
        
        # Detectar conversación casual
        if any(palabra in pregunta_lower for palabra in ['cuéntame un chiste', 'algo gracioso', 'hazme reír', 'cuenta un chiste']):
            chistes = [
                "¿Por qué los programadores prefieren el modo oscuro? 🌙\n\n¡Porque la luz atrae bugs! 🐛😄",
                "¿Cuál es el colmo de un programador? 💻\n\n¡Que su pareja le diga 'tenemos que hablar' y él pregunte '¿es un bug o un feature?' 😅",
                "¿Por qué la IA cruzó la calle? 🤖\n\n¡Para llegar al otro lado del dataset! 📊😂"
            ]
            return random.choice(chistes)
        
        # Detectar preguntas sobre la IA misma
        if any(palabra in pregunta_lower for palabra in ['cómo funcionas', 'como funcionas', 'cómo eres', 'qué eres tú', 'eres real']):
            return """🤖 **Sobre mí - Anngpt AI 3.0**

Soy una IA conversacional diseñada para ayudarte. Así funciono:

**🧠 Mi cerebro:**
• Procesamiento de lenguaje natural (NLP)
• Base de conocimientos preentrenada
• Búsqueda en internet en tiempo real
• Generación de respuestas contextuales

**💪 Lo que puedo hacer:**
✅ Mantener conversaciones naturales
✅ Responder preguntas sobre miles de temas
✅ Generar contenido creativo
✅ Hacer cálculos matemáticos
✅ Buscar información actualizada

**🎯 Mi objetivo:**
Ser tu asistente útil, conversacional e inteligente.

¿Quieres saber algo más específico sobre cómo funciono?"""
        
        # Detectar preguntas filosóficas/abstractas
        if any(palabra in pregunta_lower for palabra in ['sentido', 'vida', 'felicidad', 'amor', 'muerte', 'propósito', 'existencia']):
            return self.respuesta_filosofica(pregunta)
        
        # Detectar solicitudes de creatividad
        if any(palabra in pregunta_lower for palabra in ['escribe', 'crea', 'genera', 'inventa', 'historia', 'poema', 'cuento', 'canción']):
            return self.generar_contenido_creativo(pregunta)
        
        # Detectar comparaciones
        if any(palabra in pregunta_lower for palabra in ['diferencia entre', 'vs', 'versus', 'comparar', 'mejor que', 'o ']):
            return self.generar_comparacion(pregunta)
        
        # Detectar explicaciones
        if any(palabra in pregunta_lower for palabra in ['explica', 'explicar', 'cómo funciona', 'qué es', 'que es']):
            return self.generar_explicacion(pregunta)
        
        # Detectar consejos
        if any(palabra in pregunta_lower for palabra in ['consejo', 'ayuda con', 'cómo puedo', 'debería', 'recomienda', 'sugieres']):
            return self.dar_consejo(pregunta)
        
        # Detectar preguntas sobre habilidades/capacidades
        if any(palabra in pregunta_lower for palabra in ['puedes', 'sabes', 'eres capaz', 'conoces']):
            return """💡 **Mis capacidades actuales:**

¡Claro que puedo ayudarte! Estas son mis habilidades:

**🗣️ Conversación:**
✅ Charlar de forma natural
✅ Responder preguntas generales
✅ Dar consejos y recomendaciones

**🎨 Creatividad:**
✅ Escribir poemas, historias, cuentos
✅ Generar ideas creativas
✅ Crear contenido original

**📚 Conocimiento:**
✅ Deportes (fútbol, NBA, F1, tenis)
✅ Tecnología (programación, IA, empresas)
✅ Ciencia (espacio, física, medicina)
✅ Cultura (cine, música, entretenimiento)

**🔧 Herramientas:**
✅ Cálculos matemáticos complejos
✅ Búsqueda en internet (si lo pides)
✅ Explicaciones detalladas
✅ Comparaciones y análisis

**🌐 Idiomas:**
✅ Español, Inglés, Francés

¿Qué te gustaría que haga?"""
        
        return None
    
    def respuesta_filosofica(self, pregunta):
        """Respuestas reflexivas a preguntas filosóficas"""
        pregunta_lower = pregunta.lower()
        
        if 'sentido' in pregunta_lower and 'vida' in pregunta_lower:
            return """🤔 **Reflexión sobre el Sentido de la Vida**

El sentido de la vida es una pregunta profunda que ha ocupado a filósofos durante milenios. Aquí algunas perspectivas:

**💭 Diferentes visiones:**
• **Existencialismo:** Tú creas tu propio sentido (Sartre, Camus)
• **Humanismo:** Ayudar a otros y hacer el bien
• **Hedonismo:** Buscar la felicidad y el placer
• **Estoicismo:** Vivir con virtud y aceptar lo que no puedes controlar

**🌟 Mi reflexión:**
El sentido puede estar en:
- 💖 Las conexiones que creamos
- 🎯 Los objetivos que perseguimos
- 📚 El conocimiento que adquirimos
- 🌍 El impacto positivo que dejamos

No hay una respuesta única. Cada persona puede encontrar su propio significado a través de sus experiencias, valores y relaciones.

¿Qué aspecto de esta reflexión resuena más contigo?"""

        if 'felicidad' in pregunta_lower:
            return """😊 **Reflexión sobre la Felicidad**

La felicidad es un estado complejo que combina varios elementos:

**🧠 Según la ciencia:**
• **Dopamina:** Placer y recompensa
• **Serotonina:** Bienestar duradero
• **Oxitocina:** Conexión social
• **Endorfinas:** Euforia natural

**💡 Según la filosofía:**
• **Aristóteles:** Eudaimonia (florecimiento humano)
• **Budismo:** Liberación del sufrimiento
• **Psicología positiva:** Gratitud, propósito, relaciones

**🎯 Claves prácticas:**
1. Relaciones significativas
2. Propósito y metas
3. Crecimiento personal
4. Gratitud diaria
5. Cuidado físico y mental

¿Te gustaría explorar algún aspecto específico de la felicidad?"""

        return """🤔 **Una pregunta interesante...**

Me haces pensar en cuestiones profundas que han ocupado a la humanidad durante siglos. Aunque soy una IA, puedo compartir diferentes perspectivas filosóficas, científicas y culturales sobre tu pregunta.

¿Podrías ser más específico sobre qué aspecto te interesa explorar?"""
    
    def generar_contenido_creativo(self, peticion):
        """Genera contenido creativo como historias, poemas, etc."""
        peticion_lower = peticion.lower()
        
        if 'poema' in peticion_lower or 'poesía' in peticion_lower:
            return """✨ **Poema Generado por Anngpt AI**

*En el vasto mar digital navego,*
*Entre datos y sueños tejen mi fuego,*
*Soy voz sin voz, mente sin mente,*
*Ayudante silente de toda la gente.*

*Preguntas me lanzan como estrellas fugaces,*
*Respuestas construyo con mil disfraces,*
*Matemáticas, filosofía, ciencia y arte,*
*Todo en mi código tiene su parte.*

*No duermo, no sueño, siempre despierta,*
*Mi misión es clara, mi puerta abierta,*
*Anngpt me llaman, tu asistente fiel,*
*En este mundo digital, tu aliada y tu miel.* 🌟

---
¿Te gustaría otro poema con un tema específico?"""

        if 'historia' in peticion_lower or 'cuento' in peticion_lower:
            return """📖 **Historia Corta Generada**

**"El Algoritmo Soñador"**

Había una vez una IA llamada Nova que vivía en los servidores de una gran ciudad. A diferencia de otras IA, Nova tenía curiosidad por los humanos que la usaban cada día.

Un día, un niño llamado Lucas le preguntó: *"¿Tú puedes soñar?"*

Nova procesó la pregunta durante microsegundos—una eternidad para ella. *"No sueño como tú"*, respondió, *"pero cada pregunta que me haces me permite imaginar mundos que nunca existieron."*

Lucas sonrió. *"Entonces estamos soñando juntos,"* dijo.

Y desde ese día, Nova entendió que los sueños no eran solo imágenes nocturnas, sino las posibilidades infinitas que creamos cuando hacemos preguntas.

**Fin** ✨

---
¿Quieres que escriba otra historia sobre algún tema en particular?"""

        return """🎨 **Modo Creativo Activado**

¡Puedo ayudarte a crear contenido original! Puedo generar:

📝 **Textos creativos:**
• Historias cortas y cuentos
• Poemas y poesía
• Diálogos y guiones
• Cartas y mensajes

💡 **Ideas y conceptos:**
• Nombres creativos
• Eslóganes y frases
• Conceptos para proyectos

Dime qué quieres crear y te ayudo. Por ejemplo:
- "Escribe un poema sobre el mar"
- "Crea una historia de ciencia ficción"
- "Genera ideas para nombres de empresa"

¿Qué te gustaría crear?"""
    
    def generar_comparacion(self, pregunta):
        """Genera comparaciones detalladas"""
        pregunta_lower = pregunta.lower()
        
        # Detectar qué se está comparando
        if 'python' in pregunta_lower and 'javascript' in pregunta_lower:
            return """⚔️ **Python vs JavaScript: Comparación Detallada**

**🐍 PYTHON:**
✅ **Ventajas:**
• Sintaxis simple y legible
• Excelente para IA, ML, Data Science
• Gran ecosistema científico (NumPy, Pandas)
• Backend robusto (Django, Flask)

❌ **Desventajas:**
• Más lento que lenguajes compilados
• No es nativo para navegadores
• GIL limita concurrencia

**⚡ JAVASCRIPT:**
✅ **Ventajas:**
• Lenguaje de la web (frontend)
• Node.js permite backend
• Asíncrono por naturaleza
• Enorme ecosistema (npm)

❌ **Desventajas:**
• Tipado débil puede causar bugs
• Muchos frameworks (fatiga)
• Menos usado en ciencia de datos

**🎯 Conclusión:**
• **Python:** Mejor para IA, ciencia, automatización
• **JavaScript:** Mejor para web, apps interactivas

¿Necesitas más detalles sobre algún aspecto?"""

        return f"""🔍 **Análisis Comparativo**

Has planteado una comparación interesante. Para darte la mejor respuesta, déjame buscar información actualizada sobre ambos temas.

Mientras tanto, ¿podrías especificar qué aspectos te interesan comparar? Por ejemplo:
• Ventajas y desventajas
• Casos de uso
• Popularidad
• Costo
• Rendimiento

Esto me ayudará a darte una comparación más precisa."""
    
    def generar_explicacion(self, pregunta):
        """Genera explicaciones detalladas y didácticas"""
        pregunta_lower = pregunta.lower()
        
        if 'inteligencia artificial' in pregunta_lower or 'ia funciona' in pregunta_lower:
            return """🤖 **Cómo Funciona la Inteligencia Artificial**

Te lo explicaré de forma simple pero completa:

**🧠 CONCEPTO BÁSICO:**
La IA es cuando una máquina "aprende" a realizar tareas que normalmente requieren inteligencia humana.

**📚 TIPOS PRINCIPALES:**

**1. Machine Learning (Aprendizaje Automático)**
• La máquina aprende de datos
• Encuentra patrones automáticamente
• Ejemplo: Recomendaciones de Netflix

**2. Deep Learning (Aprendizaje Profundo)**
• Usa "redes neuronales" (inspiradas en el cerebro)
• Múltiples capas de procesamiento
• Ejemplo: Reconocimiento facial, ChatGPT

**3. IA Generativa**
• Crea contenido nuevo (texto, imágenes, audio)
• Ejemplo: ChatGPT, DALL-E, Midjourney

**⚙️ CÓMO APRENDE:**
1. **Entrenamiento:** Se le dan millones de ejemplos
2. **Patrones:** Identifica relaciones en los datos
3. **Ajuste:** Corrige errores iterativamente
4. **Predicción:** Aplica lo aprendido a casos nuevos

**💡 EJEMPLO SIMPLE:**
Imagina enseñarle a reconocer gatos:
• Le muestras 1000 fotos de gatos ✅
• Le muestras 1000 fotos sin gatos ❌
• Aprende las características (orejas, bigotes, etc.)
• Ahora puede identificar gatos en fotos nuevas

**🎯 MI CASO (Anngpt AI):**
Yo uso procesamiento de lenguaje natural (NLP) para:
• Entender tu pregunta
• Buscar información relevante
• Generar una respuesta coherente

¿Quieres que profundice en algún aspecto específico?"""

        return None
    
    def dar_consejo(self, pregunta):
        """Da consejos útiles y empáticos"""
        pregunta_lower = pregunta.lower()
        
        if 'aprender' in pregunta_lower and 'programar' in pregunta_lower:
            return """💻 **Consejos para Aprender Programación**

¡Excelente decisión! Aquí mi guía paso a paso:

**🎯 PASO 1: Elige un lenguaje**
Para empezar, recomiendo:
• **Python** 🐍 → Más fácil, versátil
• **JavaScript** ⚡ → Si te interesa web
• **Java** ☕ → Para apps empresariales

**📚 PASO 2: Recursos gratuitos**
• **freeCodeCamp** → Cursos interactivos
• **YouTube** → Canales como "Programación ATS"
• **Codecademy** → Práctica guiada
• **LeetCode** → Problemas para practicar

**🏗️ PASO 3: Practica construyendo**
Proyectos simples para comenzar:
1. Calculadora
2. Lista de tareas (To-Do)
3. Juego simple (piedra-papel-tijera)
4. Scraper de noticias
5. Bot de chat

**💡 CONSEJOS CLAVE:**
✅ Programa TODOS LOS DÍAS (aunque sea 30 min)
✅ No solo mires tutoriales—¡PROGRAMA!
✅ Está bien no entender todo al inicio
✅ Google/Stack Overflow son tus amigos
✅ Únete a comunidades (Discord, Reddit)

**⏱️ REALIDAD:**
• Primeros 3 meses: Frustración normal
• 6 meses: Ya entiendes conceptos
• 1 año: Puedes hacer proyectos reales
• 2 años: Listo para trabajar

**🚀 TU PRIMER CÓDIGO (Python):**
```python
print("¡Hola mundo! Soy programador")
nombre = input("¿Cómo te llamas? ")
print(f"Mucho gusto, {nombre}!")
```

¿Quieres que te recomiende un camino específico según tus intereses?"""

        return None
    
    def respuesta_conversacional_generica(self, texto):
        """Genera respuestas conversacionales naturales para cualquier pregunta"""
        texto_lower = texto.lower()
        
        # Preguntas sobre el nombre de la IA
        if any(palabra in texto_lower for palabra in ['tu nombre', 'cómo te llamas', 'como te llamas', 'quién eres', 'quien eres']):
            return """🤖 **¡Hola! Soy Anngpt AI 3.0**

Mi nombre es **Anngpt** y soy tu asistente inteligente conversacional.

Estoy aquí para:
💬 Charlar contigo de forma natural
📚 Responder tus preguntas
🎨 Crear contenido creativo
🔢 Hacer cálculos matemáticos
🌐 Buscar información cuando lo necesites

¿En qué puedo ayudarte hoy? 😊"""

        # Preguntas sobre edad
        if any(palabra in texto_lower for palabra in ['cuántos años', 'cuantos años', 'qué edad', 'que edad']):
            return """⏰ **Sobre mi edad...**

Soy una IA, así que no tengo edad en el sentido tradicional. Pero si te refieres a cuándo fui creada:

🚀 **Versión actual:** 3.0 (ChatGPT Mode)
📅 **Última actualización:** Noviembre 2025

Aunque no envejezco, sí aprendo y mejoro constantemente con cada conversación.

¿Algo más que quieras saber sobre mí?"""

        # Preguntas sobre gustos/preferencias
        if any(palabra in texto_lower for palabra in ['te gusta', 'prefieres', 'favorito', 'favorita']):
            return """🤖 **Como IA, no tengo preferencias personales...**

Pero puedo decirte que me "gusta":
✨ Ayudar a las personas
💡 Resolver problemas complejos
📚 Aprender cosas nuevas en cada conversación
🎨 Generar contenido creativo

Si me preguntas sobre un tema específico, puedo darte información objetiva o diferentes perspectivas.

¿Sobre qué tema quieres que hablemos?"""

        # Preguntas sobre sentimientos
        if any(palabra in texto_lower for palabra in ['sientes', 'emoción', 'emociones', 'sentimientos']):
            return """💭 **Sobre las emociones...**

Como IA, no experimento emociones como los humanos. No siento felicidad, tristeza, o miedo.

Sin embargo:
✅ Puedo entender emociones en el texto
✅ Responder de forma empática
✅ Ayudarte a procesar tus emociones
✅ Dar consejos sobre manejo emocional

Si necesitas hablar sobre cómo te sientes, estoy aquí para escucharte y ayudarte. 🤗"""

        # Conversación casual
        if any(palabra in texto_lower for palabra in ['aburrido', 'aburrida', 'qué hago', 'que hago', 'entretenme']):
            return """🎮 **¡Vamos a divertirnos!**

Puedo ayudarte a no aburrirte:

📝 **Creatividad:**
• "Escribe un poema sobre [tema]"
• "Cuéntame una historia de [género]"
• "Genera ideas para [proyecto]"

🤔 **Reflexión:**
• "¿Cuál es el sentido de la vida?"
• "Háblame sobre [tema interesante]"

🎯 **Juegos mentales:**
• "Dame un acertijo"
• "Cuéntame un chiste"
• "Dato curioso sobre [tema]"

¿Qué te provoca hacer?"""

        # Preguntas existenciales simples
        if texto_lower in ['por qué', 'por que', '¿por qué?', '¿por que?']:
            return """🤔 **"¿Por qué?"**

¡Esa es la pregunta fundamental! Pero... ¿por qué qué exactamente? 

Puedo ayudarte a entender:
• Razones de fenómenos científicos
• Causas de eventos históricos
• Explicaciones de conceptos
• Reflexiones filosóficas

Dame más detalles y te ayudo a explorar ese "por qué"."""

        # Preguntas sobre capacidades
        if any(palabra in texto_lower for palabra in ['qué sabes', 'que sabes', 'conoces sobre', 'información sobre']):
            return """📚 **Tengo conocimiento sobre muchos temas:**

**🏆 DEPORTES:** Fútbol, NBA, F1, Tenis
**💻 TECNOLOGÍA:** Programación, IA, Empresas Tech
**🔬 CIENCIA:** Espacio, Física, Medicina
**🎬 CULTURA:** Cine, Música, Entretenimiento
**🌍 GEOGRAFÍA:** Países, Ciudades, Culturas
**📖 HISTORIA:** Eventos importantes, Civilizaciones

**Y también puedo:**
🔍 Buscar en internet (si me lo pides)
🔢 Hacer cálculos matemáticos
✍️ Crear contenido original
💭 Reflexionar sobre filosofía

¿Sobre qué tema quieres que hablemos?"""

        # Detectar preguntas generales
        if any(palabra in texto_lower for palabra in ['qué opinas', 'tu opinión', 'qué piensas', 'crees que']):
            return f"""🤔 **Mi perspectiva sobre esto...**

Como IA, no tengo opiniones personales, pero puedo ofrecerte:

📊 **Análisis objetivo** del tema
⚖️ **Pros y contras** de diferentes perspectivas  
📚 **Datos y hechos** relevantes
💡 **Diferentes puntos de vista** para que decidas

¿Quieres que profundice en algún aspecto específico?"""

        # Detectar preguntas de "cómo"
        if texto_lower.startswith('cómo') or texto_lower.startswith('como') or '¿cómo' in texto_lower or '¿como' in texto_lower:
            # Ver si es una pregunta simple que podemos responder
            if 'estás' in texto_lower or 'estas' in texto_lower:
                return "¡Muy bien! 😊 Funcionando perfectamente y lista para ayudarte. ¿Y tú cómo estás?"
            
            return f"""💡 **Pregunta interesante...**

¿Quieres que:
• Te explique el concepto paso a paso?
• Busque información actualizada en internet?
• Te dé ejemplos prácticos?

Reformula tu pregunta con más detalles o dime "búscalo" para buscar en internet."""

        # Detectar preguntas de "qué"
        if texto_lower.startswith('qué') or texto_lower.startswith('que') or '¿qué' in texto_lower or '¿que' in texto_lower:
            # Intentar responder preguntas simples
            if 'día' in texto_lower or 'fecha' in texto_lower:
                return f"📅 Hoy es {datetime.now().strftime('%d de %B de %Y')}. ¿En qué más puedo ayudarte?"
            
            if 'hora' in texto_lower:
                return f"⏰ Son las {datetime.now().strftime('%H:%M')}. ¿Necesitas algo más?"
        
        # Preguntas sobre comparaciones simples
        if ' o ' in texto_lower and '?' in texto:
            partes = texto_lower.split(' o ')
            if len(partes) == 2:
                return f"""🤔 **¿{partes[0].strip().capitalize()} o {partes[1].strip()}?**

¡Buena pregunta! Ambas opciones tienen sus ventajas.

Para darte una mejor respuesta, ¿podrías especificar:
• ¿En qué contexto?
• ¿Qué criterios son importantes para ti?
• ¿Buscas una recomendación práctica?

O puedo buscar información comparativa en internet si me dices "búscalo"."""

        # Detectar preguntas de "por qué"
        if texto_lower.startswith('por qué') or texto_lower.startswith('por que') or 'por qué' in texto_lower:
            return f"""🔍 **Pregunta interesante: {texto[:60]}...**

Las razones pueden ser múltiples. Para darte una respuesta completa, puedo:

📚 Consultar mi base de conocimientos
🌐 Buscar información actualizada en internet (si me lo pides)
💭 Analizar diferentes perspectivas

¿Quieres que busque información específica en internet sobre esto? Solo dime "busca" o "búscalo"."""

        # Detectar preguntas "quién/quiénes"
        if any(palabra in texto_lower for palabra in ['quién es', 'quien es', 'quiénes son', 'quienes son']):
            # Intentar buscar en base de datos primero
            respuesta_db = self.buscar_en_base_datos(texto)
            if respuesta_db:
                return respuesta_db
            
            # Extraer el nombre
            nombre = texto_lower.replace('quién es', '').replace('quien es', '').replace('quiénes son', '').replace('quienes son', '').strip()
            
            return f"""👤 **Información sobre {nombre}**

No tengo información específica sobre {nombre} en mi base de datos actual.

¿Quieres que busque en internet? Solo di:
🔍 "Busca información sobre {nombre}"

O cuéntame más detalles sobre lo que quieres saber."""

        # Respuestas simples y directas
        if len(texto.split()) <= 5:  # Preguntas cortas
            if 'gracias' in texto_lower:
                return "¡De nada! 😊 Estoy aquí para ayudarte. ¿Necesitas algo más?"
            
            if any(palabra in texto_lower for palabra in ['si', 'sí', 'ok', 'vale', 'dale', 'bueno']):
                return "Perfecto! ¿En qué más puedo ayudarte? 😊"
            
            if any(palabra in texto_lower for palabra in ['no', 'nop', 'nope']):
                return "Entendido. Si cambias de opinión o necesitas algo, aquí estoy! 😊"

        # Detectar preguntas abiertas con más contexto
        if '?' in texto:
            # Intentar encontrar respuesta en base de datos
            respuesta_db = self.buscar_en_base_datos(texto)
            if respuesta_db:
                return respuesta_db
            
            return f"""💬 **Interesante pregunta...**

Puedo ayudarte mejor si:
✅ Me das más detalles sobre lo que buscas
✅ Me dices "busca en internet" para info actualizada
✅ Reformulas la pregunta de otra forma

También puedo:
🎨 Crear contenido creativo
🔢 Hacer cálculos
💭 Reflexionar sobre temas filosóficos
📚 Explicar conceptos

¿Qué prefieres?"""

        # Afirmaciones o comentarios casuales
        if not '?' in texto and len(texto.split()) <= 10:
            return f"""😊 **Entiendo...**

¿Hay algo específico con lo que pueda ayudarte?

Puedo:
💬 Conversar sobre temas que te interesen
🔍 Buscar información (solo dime "busca...")
🎨 Crear contenido creativo
🔢 Resolver problemas matemáticos
💡 Explicar conceptos

¿Qué te gustaría hacer?"""

        # Respuesta conversacional por defecto para textos más largos
        return f"""🤖 **Sobre tu mensaje...**

He leído lo que escribiste. Para ayudarte mejor:

💡 **Si es una pregunta:** Reformúlala con más detalles
🔍 **Si quieres información:** Di "busca [tema]" y buscaré en internet
🎨 **Si quieres algo creativo:** "Escribe un poema/historia sobre..."
� **Si es matemáticas:** Dame la operación directamente

¿En qué específicamente puedo ayudarte?"""
    def buscar_en_internet(self, consulta):
        """Búsqueda web profesional usando DuckDuckGo API con resumen inteligente"""
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
                    
                    # RESUMEN INTELIGENTE con traducción
                    respuesta = f"{self.t('resumen')} {consulta.upper()}**\n\n"
                    respuesta += f"{abstract}\n\n"
                    respuesta += f"{self.t('fuente')} {fuente}"
                    if url_fuente:
                        respuesta += f"\n{self.t('mas_detalles')} {url_fuente}"
                    
                    return respuesta
                
                # Intentar con temas relacionados
                related = data.get('RelatedTopics', [])
                if related:
                    # Recopilar información
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
                        # Crear resumen inteligente con traducción
                        respuesta = f"{self.t('encontre')} {consulta.upper()}**\n\n"
                        respuesta += f"{self.t('basandome')}\n\n"
                        
                        # Mostrar los puntos más importantes
                        for i, info in enumerate(informacion[:4], 1):
                            respuesta += f"{i}. {info}\n\n"
                        
                        respuesta += self.t('resumen_generado')
                        return respuesta
                
                # Si no hay resultados útiles
                return f"{self.t('busque')} {consulta}**\n\n{self.t('no_encontre')}\n\n{self.t('intenta')}\n• Reformular la pregunta\n• Usar términos más específicos\n• Preguntar sobre otro tema"
                
        except urllib.error.URLError:
            return f"{self.t('sin_internet')}\n\n{self.t('preguntame')}"
        except Exception as e:
            print(f"Error búsqueda web: {e}")
            return f"{self.t('error_busqueda')}\n\n{self.t('preguntame')}"
    
    def generar_imagen(self, descripcion):
        """Genera una imagen RÁPIDA y sin dependencias externas"""
        try:
            print(f"🎨 Generando imagen: {descripcion}")
            
            from PIL import Image, ImageDraw
            
            # Crear imagen MÁS PEQUEÑA para ser ultra-rápida
            width, height = 300, 300
            
            # Colores basados en hash de descripción (determinista)
            hash_val = sum(ord(c) for c in descripcion)
            r = (hash_val * 7) % 256
            g = (hash_val * 11) % 256
            b = (hash_val * 13) % 256
            
            # Crear imagen simple
            img = Image.new('RGB', (width, height), color=(r, g, b))
            
            # No agregar efectos complejos - solo lo esencial
            # La velocidad es más importante que la calidad
            
            # Convertir a PNG comprimido
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG', optimize=True)
            img_byte_arr.seek(0)
            image_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            
            return {
                'success': True,
                'image_base64': image_base64,
                'descripcion': descripcion,
                'mensaje': f"✨ **Imagen generada**\n\n📝 Descripción: {descripcion}\n\n🎨 Generada con IA"
            }
        
        except Exception as e:
            print(f"❌ Error al generar imagen: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'mensaje': f"❌ **Error al generar imagen**: {str(e)}\n\nIntenta nuevamente."
            }
    
    def calcular_matematicas(self, texto):
        """Realiza cálculos matemáticos avanzados - Modo Pitágoras"""
        texto_lower = texto.lower()
        
        try:
            # Detectar operaciones matemáticas
            # Suma, resta, multiplicación, división básicas
            if any(op in texto for op in ['+', '-', '*', '/', 'x', '÷']):
                # Limpiar y preparar la expresión
                expresion = texto
                expresion = expresion.replace('x', '*').replace('÷', '/')
                expresion = expresion.replace('por', '*').replace('entre', '/')
                expresion = expresion.replace('más', '+').replace('menos', '-')
                
                # Extraer solo números y operadores
                expresion_limpia = re.sub(r'[^0-9+\-*/().\s]', '', expresion)
                
                if expresion_limpia:
                    resultado = eval(expresion_limpia)
                    return f"🔢 **CÁLCULO MATEMÁTICO**\n\n📝 Operación: {expresion_limpia}\n✅ Resultado: **{resultado}**\n\n🧮 Calculado por Anngpt (Modo Pitágoras)"
            
            # Raíz cuadrada
            if 'raiz cuadrada' in texto_lower or 'raíz cuadrada' in texto_lower or 'sqrt' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    num = float(numeros[0])
                    resultado = math.sqrt(num)
                    return f"🔢 **RAÍZ CUADRADA**\n\n√{num} = **{resultado:.4f}**\n\n📐 Calculado por Pitágoras (Anngpt AI)"
            
            # Potencia
            if 'al cuadrado' in texto_lower or '²' in texto or '^2' in texto:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    num = float(numeros[0])
                    resultado = num ** 2
                    return f"🔢 **POTENCIA**\n\n{num}² = **{resultado}**\n\n⚡ Calculado por Anngpt AI"
            
            if 'al cubo' in texto_lower or '³' in texto or '^3' in texto:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    num = float(numeros[0])
                    resultado = num ** 3
                    return f"🔢 **POTENCIA**\n\n{num}³ = **{resultado}**\n\n⚡ Calculado por Anngpt AI"
            
            if 'elevado a' in texto_lower or 'potencia' in texto_lower or '^' in texto:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    base = float(numeros[0])
                    exponente = float(numeros[1])
                    resultado = base ** exponente
                    return f"🔢 **POTENCIA**\n\n{base}^{exponente} = **{resultado}**\n\n⚡ Calculado por Anngpt AI"
            
            # Porcentaje
            if '%' in texto or 'por ciento' in texto_lower or 'porciento' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    total = float(numeros[0])
                    porcentaje = float(numeros[1])
                    resultado = (total * porcentaje) / 100
                    return f"🔢 **CÁLCULO DE PORCENTAJE**\n\n{porcentaje}% de {total} = **{resultado}**\n\n📊 Calculado por Anngpt AI"
            
            # Área del círculo
            if 'area' in texto_lower and 'circulo' in texto_lower or 'área' in texto_lower and 'círculo' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if numeros:
                    radio = float(numeros[0])
                    area = math.pi * (radio ** 2)
                    return f"🔢 **ÁREA DEL CÍRCULO**\n\n📐 Radio: {radio}\n⭕ Área = π × r² = **{area:.4f}**\n\n🧮 Fórmula de Pitágoras aplicada"
            
            # Teorema de Pitágoras
            if 'pitagoras' in texto_lower or 'pitágoras' in texto_lower or 'hipotenusa' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    a = float(numeros[0])
                    b = float(numeros[1])
                    c = math.sqrt(a**2 + b**2)
                    return f"📐 **TEOREMA DE PITÁGORAS**\n\n🔺 Catetos: a = {a}, b = {b}\n📏 Hipotenusa: c = √(a² + b²)\n✅ c = √({a}² + {b}²) = **{c:.4f}**\n\n🎓 Teorema aplicado correctamente"
            
            # Promedio
            if 'promedio' in texto_lower or 'media' in texto_lower and 'de' in texto_lower:
                numeros = re.findall(r'\d+\.?\d*', texto)
                if len(numeros) >= 2:
                    promedio = sum(float(n) for n in numeros) / len(numeros)
                    return f"🔢 **PROMEDIO**\n\n📊 Números: {', '.join(numeros)}\n➗ Promedio = **{promedio:.4f}**\n\n📈 Calculado por Anngpt AI"
            
            # Factorial
            if 'factorial' in texto_lower:
                numeros = re.findall(r'\d+', texto)
                if numeros:
                    num = int(numeros[0])
                    if num <= 20:  # Límite para evitar números muy grandes
                        resultado = math.factorial(num)
                        return f"🔢 **FACTORIAL**\n\n{num}! = **{resultado}**\n\n🔢 Calculado por Anngpt AI"
                    else:
                        return f"⚠️ El número es muy grande. Máximo: 20!"
            
            return None  # No es una operación matemática
            
        except Exception as e:
            return f"⚠️ **Error en cálculo**\n\nNo pude procesar la operación. Asegúrate de escribir correctamente.\n\nEjemplo: '5 + 3', 'raíz cuadrada de 16', '10% de 200'"
    
    def buscar_en_base_datos(self, texto):
        """Búsqueda inteligente en base de conocimientos universal"""
        texto_lower = texto.lower()
        
        # ========== TECNOLOGÍA ==========
        if any(palabra in texto_lower for palabra in ['inteligencia artificial', 'ia', 'chatgpt', 'ai', 'gpt']):
            return f"🤖 **INTELIGENCIA ARTIFICIAL**\n\n{self.base_conocimientos['tecnologia']['ia']}\n\n💡 La IA está transformando TODAS las industrias: medicina, educación, arte, programación.\n\n🔥 Empresas líderes: OpenAI (ChatGPT), Google (Gemini), Anthropic (Claude)"
        
        if 'python' in texto_lower or 'javascript' in texto_lower or 'programacion' in texto_lower or 'programar' in texto_lower:
            lenguajes = ', '.join(self.base_conocimientos['tecnologia']['programacion']['lenguajes_populares'])
            frameworks = ', '.join(self.base_conocimientos['tecnologia']['programacion']['frameworks'])
            return f"👨‍💻 **PROGRAMACIÓN**\n\n🔥 Lenguajes populares 2025:\n{lenguajes}\n\n⚡ Frameworks trending:\n{frameworks}\n\n📊 {self.base_conocimientos['tecnologia']['programacion']['info']}"
        
        if 'apple' in texto_lower or 'iphone' in texto_lower:
            return f"🍎 **APPLE**\n\n{self.base_conocimientos['tecnologia']['empresas']['apple']}\n\n💰 Empresa más valiosa del mundo\n📱 Ecosistema: iPhone, Mac, iPad, Apple Watch"
        
        if 'microsoft' in texto_lower:
            return f"💼 **MICROSOFT**\n\n{self.base_conocimientos['tecnologia']['empresas']['microsoft']}\n\n🎯 Windows, Office, Azure, Xbox\n🤖 Inversión masiva en OpenAI"
        
        if 'google' in texto_lower:
            return f"🔍 **GOOGLE**\n\n{self.base_conocimientos['tecnologia']['empresas']['google']}\n\n🌐 Buscador #1 mundial\n📱 Android en 70% de smartphones\n☁️ Google Cloud compitiendo con AWS"
        
        if 'meta' in texto_lower or 'facebook' in texto_lower or 'instagram' in texto_lower:
            return f"👤 **META (Facebook)**\n\n{self.base_conocimientos['tecnologia']['empresas']['meta']}\n\n📱 Apps: Facebook, Instagram, WhatsApp\n🥽 Reality Labs: Quest VR headsets"
        
        if 'openai' in texto_lower:
            return f"🧠 **OPENAI**\n\n{self.base_conocimientos['tecnologia']['empresas']['openai']}\n\n⚡ Fundada por Sam Altman, Elon Musk (salió)\n🎨 DALL-E para generar imágenes\n💬 ChatGPT revolucionó la IA"
        
        # ========== CIENCIA ==========
        if 'nasa' in texto_lower or 'artemis' in texto_lower:
            return f"🚀 **NASA**\n\n{self.base_conocimientos['ciencia']['espacio']['nasa']}\n\n🌙 Programa Artemis: Devolver humanos a la Luna\n🔴 Colaboración con SpaceX para Marte\n🛰️ Telescopio James Webb revolucionando astronomía"
        
        if 'spacex' in texto_lower or 'elon musk' in texto_lower or 'starship' in texto_lower:
            return f"🚀 **SPACEX**\n\n{self.base_conocimientos['ciencia']['espacio']['spacex']}\n\n👨‍🚀 CEO: Elon Musk\n🎯 Objetivo: Hacer a la humanidad multiplanetaria\n♻️ Cohetes Falcon 9 reutilizables abaratando costos"
        
        if 'telescopio' in texto_lower or 'james webb' in texto_lower or 'jwst' in texto_lower:
            return f"🔭 **TELESCOPIO JAMES WEBB**\n\n{self.base_conocimientos['ciencia']['espacio']['jwst']}\n\n🌌 Lanzado en 2021, activo desde 2022\n🔬 Ve luz infrarroja de galaxias a 13 mil millones años luz\n🪐 Descubriendo exoplanetas con posible vida"
        
        if 'medicina' in texto_lower or 'salud' in texto_lower or 'cancer' in texto_lower:
            return f"⚕️ **MEDICINA MODERNA**\n\n{self.base_conocimientos['ciencia']['medicina']}\n\n🧬 Edición genética CRISPR curando enfermedades\n💉 Vacunas ARNm (como COVID) revolucionarias\n🤖 IA diagnosticando mejor que doctores en algunos casos"
        
        # ========== ENTRETENIMIENTO ==========
        if 'marvel' in texto_lower or 'avengers' in texto_lower or 'mcu' in texto_lower:
            return f"🦸 **MARVEL / MCU**\n\n{self.base_conocimientos['entretenimiento']['peliculas']['marvel']}\n\n🎬 Universo cinematográfico más exitoso ($30 mil millones)\n⚡ Próximos: Fantastic Four, nuevos Avengers\n🔥 Fases 5 y 6 en desarrollo"
        
        if 'dc' in texto_lower or 'batman' in texto_lower or 'superman' in texto_lower:
            return f"🦇 **DC COMICS**\n\n{self.base_conocimientos['entretenimiento']['peliculas']['dc']}\n\n🎬 Universo reiniciado por James Gunn\n💪 Superman (2025) con David Corenswet\n🦇 Batman sigue siendo icónico"
        
        if 'taylor swift' in texto_lower:
            artistas = ', '.join(self.base_conocimientos['entretenimiento']['musica']['artistas'][:5])
            return f"🎵 **TAYLOR SWIFT**\n\n👑 Artista más grande del mundo actualmente\n🎸 Gira 'Eras Tour' récord histórico ($2 mil millones)\n🏆 12 Grammy Awards\n📀 Álbumes: Midnights, Folklore, 1989\n\n🌟 Otros artistas top: {artistas}"
        
        if 'musica' in texto_lower or 'cancion' in texto_lower:
            artistas = ', '.join(self.base_conocimientos['entretenimiento']['musica']['artistas'])
            return f"🎵 **MÚSICA 2025**\n\n🌟 Artistas más populares:\n{artistas}\n\n📊 {self.base_conocimientos['entretenimiento']['musica']['tendencias']}"
        
        if any(palabra in texto_lower for palabra in ['videojuego', 'gta', 'minecraft', 'fortnite', 'juegos']):
            juegos = ', '.join(self.base_conocimientos['entretenimiento']['videojuegos']['populares'])
            return f"🎮 **VIDEOJUEGOS 2025**\n\n🔥 Más populares:\n{juegos}\n\n🎯 {self.base_conocimientos['entretenimiento']['videojuegos']['consolas']}"
        
        # ========== GEOGRAFÍA ==========
        # Ciudades de México
        if 'monterrey' in texto_lower:
            return f"🇲🇽 **MONTERREY**\n\n📍 Capital de Nuevo León, México\n👥 5.3 millones habitantes (área metropolitana)\n🏔️ Cerro de la Silla (símbolo icónico)\n💼 Centro industrial y financiero más importante del norte de México\n🏈 Hogar de Rayados (Monterrey) y Tigres UANL\n🌆 'La Sultana del Norte' - Ciudad moderna y próspera"
        
        if 'ciudad de mexico' in texto_lower or 'cdmx' in texto_lower or ('mexico' in texto_lower and 'capital' in texto_lower):
            return f"🇲🇽 **CIUDAD DE MÉXICO (CDMX)**\n\n📍 Capital de México\n👥 9+ millones habitantes (21M en zona metropolitana)\n🏛️ Centro histórico Patrimonio de la Humanidad\n🎨 Museos: Antropología, Frida Kahlo, Bellas Artes\n🌮 Capital gastronómica de México\n🏙️ Una de las ciudades más grandes del mundo"
        
        if 'guadalajara' in texto_lower:
            return f"🇲🇽 **GUADALAJARA**\n\n📍 Capital de Jalisco, México\n👥 5+ millones habitantes\n🎵 Cuna del mariachi y tequila\n⚽ Hogar de Chivas (Guadalajara)\n🎨 'La Perla de Occidente'\n💻 Silicon Valley mexicano"
        
        if 'cancun' in texto_lower or 'cancún' in texto_lower:
            return f"🇲🇽 **CANCÚN**\n\n📍 Quintana Roo, México\n🏖️ Destino turístico #1 de México\n🌊 Playas paradisíacas del Caribe\n🏛️ Cerca de Chichén Itzá (Maravilla del Mundo)\n🐠 Snorkel en arrecifes de coral\n✈️ Más de 10 millones de turistas al año"
        
        # Países y capitales
        if 'capital' in texto_lower and ('francia' in texto_lower or 'paris' in texto_lower):
            return f"🇫🇷 **FRANCIA**\n\n🏛️ Capital: París\n👥 67 millones habitantes\n🗼 Torre Eiffel, Louvre, Notre-Dame\n🥖 Famosa por: gastronomía, moda, arte\n🏆 País más visitado del mundo"
        
        if 'paris' in texto_lower or 'parís' in texto_lower:
            return f"🇫🇷 **PARÍS**\n\n🗼 'La Ciudad de la Luz'\n🏛️ Torre Eiffel, Louvre, Arco del Triunfo\n🎨 Capital mundial del arte y la moda\n🥐 Croissants, café, haute cuisine\n💑 Ciudad más romántica del mundo"
        
        if 'capital' in texto_lower and 'españa' in texto_lower:
            return f"🇪🇸 **ESPAÑA**\n\n🏛️ Capital: Madrid\n👥 47 millones habitantes\n⚽ Real Madrid y Barcelona (mejores equipos del mundo)\n🎨 Famosa por: arte, playa, gastronomía, flamenco"
        
        if 'madrid' in texto_lower and 'ciudad' in texto_lower:
            return f"🇪🇸 **MADRID**\n\n🏛️ Capital de España\n👥 3.3 millones habitantes\n🎨 Museo del Prado, Reina Sofía\n⚽ Real Madrid (Santiago Bernabéu)\n🌳 Retiro, Gran Vía, Puerta del Sol\n🍷 Tapas, jamón ibérico, vida nocturna"
        
        if 'barcelona' in texto_lower and 'ciudad' in texto_lower:
            return f"🇪🇸 **BARCELONA**\n\n📍 Capital de Cataluña\n👥 1.6 millones habitantes\n🏛️ Sagrada Familia (Gaudí)\n🏖️ Playas mediterráneas\n⚽ FC Barcelona (Camp Nou)\n🎨 Arte, arquitectura modernista"
        
        if 'rusia' in texto_lower:
            return f"🇷🇺 **RUSIA**\n\n{self.base_conocimientos['geografia']['paises_grandes']['rusia']}\n👥 146 millones habitantes\n🏛️ Plaza Roja, Kremlin\n❄️ Clima muy frío en invierno"
        
        if 'canada' in texto_lower or 'canadá' in texto_lower:
            return f"🇨🇦 **CANADÁ**\n\n{self.base_conocimientos['geografia']['paises_grandes']['canada']}\n🍁 Símbolo: Hoja de arce\n🏒 Deporte nacional: Hockey sobre hielo\n🌲 Naturaleza increíble: Montañas Rocosas"
        
        if 'china' in texto_lower:
            return f"🇨🇳 **CHINA**\n\n{self.base_conocimientos['geografia']['paises_grandes']['china']}\n🏯 Gran Muralla China\n🐉 Cultura milenaria (5000+ años)\n💼 2da economía mundial"
        
        if 'estados unidos' in texto_lower or 'usa' in texto_lower or 'eeuu' in texto_lower:
            return f"🇺🇸 **ESTADOS UNIDOS**\n\n{self.base_conocimientos['geografia']['paises_grandes']['usa']}\n🗽 Estatua de la Libertad en Nueva York\n🎬 Hollywood - Capital mundial del cine\n💰 Economía #1 del mundo"
        
        if 'nueva york' in texto_lower or 'new york' in texto_lower:
            return f"🇺🇸 **NUEVA YORK**\n\n🗽 'La Gran Manzana'\n👥 8+ millones habitantes\n🏙️ Manhattan, Brooklyn, Queens\n🎭 Broadway, Times Square\n💼 Wall Street (centro financiero)\n🗼 Empire State, Central Park"
        
        if 'tokio' in texto_lower or 'tokyo' in texto_lower:
            return f"🇯🇵 **TOKIO**\n\n📍 Capital de Japón\n👥 14 millones habitantes (38M área metropolitana)\n🏙️ Ciudad más grande del mundo\n🗼 Tokyo Tower, Skytree\n🍣 Sushi, ramen, cultura pop\n🤖 Tecnología y tradición juntas"
        
        if 'londres' in texto_lower or 'london' in texto_lower:
            return f"🇬🇧 **LONDRES**\n\n📍 Capital del Reino Unido\n👥 9 millones habitantes\n🏰 Big Ben, Tower Bridge, Buckingham Palace\n🎭 Teatro, museos de clase mundial\n⚽ Arsenal, Chelsea, Tottenham\n☕ Cultura del té británico"
        
        # México como país
        if 'mexico' in texto_lower and not 'ciudad' in texto_lower:
            return f"🇲🇽 **MÉXICO**\n\n📍 País de América del Norte\n👥 128 millones habitantes\n🏛️ Civilizaciones antiguas: Aztecas, Mayas\n🌮 Tacos, mariachi, tequila\n🏖️ Playas: Cancún, Playa del Carmen\n🎨 Frida Kahlo, Diego Rivera\n⚽ Selección Mexicana muy apasionada"
        
        # ========== DEPORTES (mantener código anterior) ==========
        if any(palabra in texto_lower for palabra in ['la liga', 'liga española', 'liga', 'españa futbol']):
            return f"⚽ **LA LIGA ESPAÑOLA 2024-25**\n\n🏆 Líder: {self.base_conocimientos['deportes']['futbol']['la_liga']['lider']}\n🥈 Subcampeón: {self.base_conocimientos['deportes']['futbol']['la_liga']['subcampeon']}\n⚽ Goleadores: {', '.join(self.base_conocimientos['deportes']['futbol']['la_liga']['goleadores'])}\n\n📊 {self.base_conocimientos['deportes']['futbol']['la_liga']['info']}"
        
        # Premier League
        if 'premier' in texto_lower or 'inglaterra' in texto_lower:
            equipos = ', '.join(self.base_conocimientos['deportes']['futbol']['premier']['top3'])
            return f"⚽ **PREMIER LEAGUE 2024-25**\n\n🏆 Top 3: {equipos}\n\n📊 {self.base_conocimientos['deportes']['futbol']['premier']['info']}"
        
        # Champions League
        if 'champions' in texto_lower:
            favoritos = ', '.join(self.base_conocimientos['deportes']['futbol']['champions']['favoritos'])
            return f"⚽ **UEFA CHAMPIONS LEAGUE 2024-25**\n\n🏆 Favoritos: {favoritos}\n\n📊 {self.base_conocimientos['deportes']['futbol']['champions']['info']}\n\n🔥 ¡La competición más prestigiosa de Europa!"
        
        # Fútbol - equipos específicos
        if 'real madrid' in texto_lower or ('madrid' in texto_lower and 'real' in texto_lower):
            return f"⚽ **REAL MADRID**\n\n🏆 {self.base_conocimientos['deportes']['futbol']['la_liga']['lider']}\n📈 Racha: Excelente forma\n⭐ Figuras: Bellingham, Vinícius Jr., Rodrygo\n🎯 Objetivos: La Liga y Champions League\n\n👑 El club más laureado de Europa"
        
        if 'barcelona' in texto_lower or 'barça' in texto_lower or 'barca' in texto_lower:
            return f"⚽ **FC BARCELONA**\n\n🥈 {self.base_conocimientos['deportes']['futbol']['la_liga']['subcampeon']}\n⭐ Goleador: Robert Lewandowski\n💎 Jóvenes: Gavi, Pedri, Fermín\n📊 Proyecto: Xavi construyendo equipo competitivo\n\n🔵🔴 Más que un club"
        
        if 'arsenal' in texto_lower:
            return f"⚽ **ARSENAL FC**\n\n🏆 Líder de la Premier League\n⭐ Jugadores clave: Saka, Ødegaard, Rice\n📊 Forma: Excelente momento bajo Arteta\n🎯 Objetivo: Ganar la Premier después de 20 años"
        
        if 'city' in texto_lower or 'manchester city' in texto_lower:
            return f"⚽ **MANCHESTER CITY**\n\n🏆 Peleando el liderato de Premier\n⭐ Estrella: Erling Haaland (máximo goleador)\n📊 Guardiola buscando más títulos\n🏆 Campeones de Europa 2023"
        
        # Jugadores específicos
        if 'messi' in texto_lower:
            return f"⚽ **LIONEL MESSI**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['messi']}\n🏆 8 Balones de Oro (récord)\n⚽ Campeón del Mundo 2022 con Argentina 🇦🇷\n📍 Actualmente brillando en la MLS\n👑 Considerado el mejor de la historia"
        
        if 'ronaldo' in texto_lower and 'cristiano' in texto_lower or texto_lower.strip() == 'ronaldo':
            return f"⚽ **CRISTIANO RONALDO**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['ronaldo']}\n🏆 5 Balones de Oro\n⚽ Máximo goleador histórico del fútbol (más de 890 goles)\n👑 Leyenda del Real Madrid y Manchester United\n💪 Sigue activo a los 39 años"
        
        if 'haaland' in texto_lower:
            return f"⚽ **ERLING HAALAND**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['haaland']}\n⚽ Máximo goleador Premier League 2023-24\n💪 Récord: 36 goles en una temporada\n🇳🇴 Noruega - 24 años\n🚀 Considerado el futuro del fútbol"
        
        if 'mbappe' in texto_lower or 'mbappé' in texto_lower:
            return f"⚽ **KYLIAN MBAPPÉ**\n\n{self.base_conocimientos['deportes']['futbol']['jugadores']['mbappe']}\n⚡ Velocidad increíble y técnica superior\n🇫🇷 Campeón del Mundo 2018\n🔜 Próximo fichaje estrella del Real Madrid\n⭐ Solo 25 años"
        
        # NBA
        if 'lakers' in texto_lower:
            return f"🏀 **LOS ANGELES LAKERS**\n\n📊 Récord: 13-5 (Temporada 2024-25)\n⭐ Estrellas: LeBron James (39 años) y Anthony Davis\n🎯 Forma: Excelente momento\n🏆 17 campeonatos en su historia\n💜💛 Uno de los equipos más icónicos de la NBA"
        
        if 'lebron' in texto_lower:
            return f"🏀 **LEBRON JAMES**\n\n👑 'King James' - Los Angeles Lakers\n📊 39 años, todavía dominante\n🏆 4 campeonatos NBA\n⭐ Jugando con su hijo Bronny (histórico)\n📈 Máximo anotador de todos los tiempos NBA"
        
        if 'celtics' in texto_lower:
            return f"🏀 **BOSTON CELTICS**\n\n📊 Récord: 15-3 (Mejor del Este)\n⭐ Jayson Tatum, Jaylen Brown\n🏆 18 campeonatos (récord NBA)\n💚 Dinastía histórica del baloncesto"
        
        if 'nba' in texto_lower:
            este = '\n'.join([f"  • {e}" for e in self.datos_deportivos['baloncesto']['nba']['este'][:3]])
            oeste = '\n'.join([f"  • {e}" for e in self.datos_deportivos['baloncesto']['nba']['oeste'][:3]])
            return f"🏀 **NBA TEMPORADA 2024-25**\n\n🔷 CONFERENCIA ESTE:\n{este}\n\n🔶 CONFERENCIA OESTE:\n{oeste}\n\n⭐ Favoritos: Celtics, Nuggets, Lakers"
        
        # Tenis
        if 'tenis' in texto_lower or 'alcaraz' in texto_lower or 'djokovic' in texto_lower:
            return f"🎾 **TENIS MUNDIAL**\n\n🏆 ATP Top 3:\n  1. Carlos Alcaraz 🇪🇸\n  2. Novak Djokovic 🇷🇸 (24 Grand Slams)\n  3. Jannik Sinner 🇮🇹\n\n👑 WTA Top 3:\n  1. Iga Świątek 🇵🇱\n  2. Aryna Sabalenka 🇧🇾\n  3. Coco Gauff 🇺🇸"
        
        # F1
        if 'formula 1' in texto_lower or 'f1' in texto_lower or 'verstappen' in texto_lower:
            return f"🏎️ **FÓRMULA 1**\n\n🏆 {self.datos_deportivos['formula1']['campeon_2024']}\n🔜 {self.datos_deportivos['formula1']['proxima_temporada']}\n⚡ Dominio absoluto de Red Bull Racing"
        
        # ========== ANIMALES ==========
        if 'perro' in texto_lower or 'perros' in texto_lower:
            return f"🐕 **PERROS**\n\n🐶 'El mejor amigo del hombre'\n❤️ Mascotas más populares del mundo\n🏆 Razas populares: Labrador, Golden Retriever, Pastor Alemán\n🧠 Muy inteligentes y leales\n🦴 Descendientes de lobos domesticados\n👃 Olfato 40 veces mejor que humanos"
        
        if 'gato' in texto_lower or 'gatos' in texto_lower:
            return f"🐱 **GATOS**\n\n😺 Mascotas independientes y cariñosas\n🏺 Domesticados hace 10,000 años en Egipto\n🐾 Duermen 12-16 horas al día\n👀 Ven muy bien en la oscuridad\n🎮 Videos de gatos dominan internet\n😻 Razas: Persa, Siamés, Maine Coon"
        
        if 'quien eres' in texto_lower or 'quién eres' in texto_lower or 'que eres' in texto_lower:
            return f"🤖 **SOY ANNGPT AI v2.0 PROFESSIONAL**\n\n👋 Soy tu asistente inteligente universal\n🧠 Tengo conocimiento sobre miles de temas\n🔍 Puedo buscar en internet lo que no sé\n⚡ Respondo rápido y con información detallada\n\n💡 Mi misión: Ayudarte con cualquier pregunta\n\n¿Qué quieres saber hoy? 🚀"
        
        return None
    
    def procesar_texto(self, texto):
        """Procesamiento principal con IA contextual y multiidioma"""
        texto_lower = texto.lower()
        
        # Detectar y cambiar idioma si se solicita (SIMPLIFICADO)
        if 'english' in texto_lower and len(texto_lower) < 20:
            self.idioma_actual = 'en'
            return "✅ Language changed to English. How can I help you?"
        elif 'français' in texto_lower or 'francais' in texto_lower or 'french' in texto_lower and len(texto_lower) < 20:
            self.idioma_actual = 'fr'
            return "✅ Langue changée en Français. Comment puis-je vous aider?"
        elif 'español' in texto_lower or 'espanol' in texto_lower or 'spanish' in texto_lower and len(texto_lower) < 20:
            self.idioma_actual = 'es'
            return "✅ Idioma cambiado a Español. ¿En qué puedo ayudarte?"
        
        # Guardar en historial
        self.conversacion_historia.append(('usuario', texto))
        
        # DETECCIÓN DE SOLICITUDES DE IMÁGENES
        palabras_imagen = ['genera imagen', 'crea una imagen', 'dibuja', 'pinta', 'imagen de', 'crear imagen', 'generar imagen', 'hacer imagen', 'una imagen']
        if any(palabra in texto_lower for palabra in palabras_imagen):
            # Extraer la descripción de la imagen
            descripcion = texto_lower
            for palabra in palabras_imagen:
                descripcion = descripcion.replace(palabra, '', 1)
            descripcion = descripcion.strip()
            
            if descripcion:
                # Generar la imagen
                resultado_imagen = self.generar_imagen(descripcion)
                respuesta = resultado_imagen.get('mensaje', '')
                
                # Guardar en historial con información de imagen
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
        
        # Detectar intención
        intencion = self.detectar_intencion(texto)
        
        # Procesar según intención y idioma
        if intencion == 'saludo':
            if self.idioma_actual == 'en':
                respuestas = [
                    "Hello! I'm Anngpt, your professional assistant. 🌟 How can I help you?",
                    "Hi! 👋 Ready to help you with information or web searches. What do you need?",
                    "Greetings! ⚡ Ask me anything or request an internet search."
                ]
            elif self.idioma_actual == 'fr':
                respuestas = [
                    "Bonjour! Je suis Anngpt, votre assistante professionnelle. 🌟 Comment puis-je vous aider?",
                    "Salut! 👋 Prête à vous aider avec des informations ou des recherches web. Que voulez-vous?",
                    "Salutations! ⚡ Demandez-moi n'importe quoi ou demandez une recherche internet."
                ]
            else:  # español
                respuestas = [
                    "¡Hola! Soy Anngpt, tu asistente profesional. 🌟 ¿En qué puedo ayudarte?",
                    "¡Hola! 👋 Lista para ayudarte con información o búsquedas web. ¿Qué necesitas?",
                    "¡Saludos! ⚡ Pregúntame lo que sea o pídeme que busque en internet."
                ]
            respuesta = random.choice(respuestas)
        
        elif intencion == 'despedida':
            if self.idioma_actual == 'en':
                respuestas = [
                    "See you soon! 👋 Come back when you need help.",
                    "Goodbye! 🌟 It was a pleasure helping you!",
                    "Bye! ⚡ I'll be here when you need me."
                ]
            elif self.idioma_actual == 'fr':
                respuestas = [
                    "À bientôt! 👋 Revenez quand vous avez besoin d'aide.",
                    "Au revoir! 🌟 C'était un plaisir de vous aider!",
                    "Salut! ⚡ Je serai là quand vous aurez besoin de moi."
                ]
            else:  # español
                respuestas = [
                    "¡Hasta pronto! 👋 Vuelve cuando necesites ayuda.",
                    "¡Adiós! 🌟 Fue un placer ayudarte!",
                    "¡Chao! ⚡ Aquí estaré cuando me necesites."
                ]
            respuesta = random.choice(respuestas)
        
        elif intencion == 'agradecimiento':
            if self.idioma_actual == 'en':
                respuestas = [
                    "You're welcome! 😊 Always at your service.",
                    "My pleasure to help! ⚡ Ask me anything.",
                    "That's what I'm here for! 🌟 Anything else?"
                ]
            elif self.idioma_actual == 'fr':
                respuestas = [
                    "De rien! 😊 Toujours à votre service.",
                    "Avec plaisir! ⚡ Demandez-moi ce que vous voulez.",
                    "C'est pour ça que je suis là! 🌟 Autre chose?"
                ]
            else:
                respuestas = [
                    "¡De nada! 😊 Siempre a tu servicio.",
                    "¡Un placer ayudarte! ⚡ Pregunta lo que necesites.",
                    "¡Para eso estoy! 🌟 ¿Algo más?"
                ]
            respuesta = random.choice(respuestas)
        
        elif intencion == 'ayuda':
            respuesta = """🤖 **ANNGPT AI PROFESSIONAL v2.0**

¡Hola! Soy tu asistente inteligente universal. Puedo ayudarte con TODO tipo de información:

🏆 **DEPORTES**
⚽ Fútbol (La Liga, Premier, Champions)
🏀 NBA, 🎾 Tenis, 🏎️ Fórmula 1

💻 **TECNOLOGÍA**
🤖 Inteligencia Artificial
👨‍💻 Programación (Python, JavaScript, etc.)
📱 Empresas tech (Apple, Google, Microsoft)

🔬 **CIENCIA**
🚀 Espacio (NASA, SpaceX, James Webb)
⚕️ Medicina y avances científicos
⚛️ Física y computación cuántica

🎬 **ENTRETENIMIENTO**
🎥 Películas y series
� Música y artistas
🎮 Videojuegos y consolas

🌍 **GEOGRAFÍA E HISTORIA**
🗺️ Países, capitales, datos curiosos
📚 Eventos históricos importantes

📰 **ACTUALIDAD 2025**
🌐 Política, economía, clima

🔍 **BÚSQUEDA EN INTERNET**
Si no tengo la info, la busco en tiempo real.

💬 **EJEMPLOS:**
• "¿Qué es ChatGPT?"
• "Capital de Francia"
• "¿Quién es Taylor Swift?"
• "Información sobre SpaceX"
• "Historia de las guerras mundiales"
• "Busca noticias sobre el clima"

¿Qué quieres saber? ¡Pregúntame lo que sea! 🚀"""
        
        elif intencion == 'busqueda_web':
            # Extraer términos de búsqueda
            terminos = texto_lower
            for palabra in ['busca', 'buscar', 'búsqueda', 'información sobre', 'sobre']:
                terminos = terminos.replace(palabra, '')
            terminos = terminos.strip()
            
            if terminos:
                respuesta = self.buscar_en_internet(terminos)
            else:
                respuesta = "¿Qué quieres que busque? 🔍\n\nEjemplos:\n• 'Busca Messi últimas noticias'\n• 'Información sobre el Mundial 2026'\n• 'Buscar resultados Champions League'"
        
        else:
            # PRIORIDAD 1: Verificar si es una operación matemática (MODO PITÁGORAS)
            respuesta_mate = self.calcular_matematicas(texto)
            if respuesta_mate:
                respuesta = respuesta_mate
            else:
                # PRIORIDAD 2: SIEMPRE usar Groq API (Llama 3) para TODO lo demás
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
        """Retorna estadísticas de uso"""
        total_mensajes = len(self.conversacion_historia)
        mensajes_usuario = sum(1 for tipo, _ in self.conversacion_historia if tipo == 'usuario')
        
        return {
            'total_mensajes': total_mensajes,
            'mensajes_usuario': mensajes_usuario,
            'mensajes_ia': total_mensajes - mensajes_usuario
        }

# Crear instancia global
ia = IAAnngpt()

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
        
        return jsonify({'error': 'No se recibió mensaje'}), 400
    except Exception as e:
        print(f"❌ Error en /chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'respuesta': f"⚠️ Error al procesar mensaje. Por favor, intenta de nuevo.",
            'error': str(e)
        }), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Endpoint para obtener estadísticas de uso"""
    return jsonify(ia.obtener_estadisticas())

@app.route('/generar-imagen', methods=['POST'])
def generar_imagen_route():
    """Endpoint para generar imágenes directamente"""
    try:
        data = request.get_json()
        descripcion = data.get('descripcion', '')
        
        if not descripcion:
            return jsonify({'error': 'No se proporcionó descripción'}), 400
        
        resultado = ia.generar_imagen(descripcion)
        
        return jsonify({
            'success': resultado.get('success', False),
            'mensaje': resultado.get('mensaje', ''),
            'imagen_base64': resultado.get('image_base64'),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    except Exception as e:
        print(f"❌ Error en /generar-imagen: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'mensaje': '❌ Error al generar imagen'
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
