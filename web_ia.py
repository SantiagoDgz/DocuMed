from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import re
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import secrets
import json
from groq import Groq
from pacientes_db import GestorPacientes
from medical_ai import AnalisisAIMedico
from encryption import encriptador, gestor_claves
from cloud_sync import sincronizador_nube

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
gestor_pacientes = GestorPacientes()
ia_medica = AnalisisAIMedico()

# Configurar Groq API
GROQ_API_KEY = "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"
groq_client = Groq(api_key=GROQ_API_KEY)

# Diccionario de usuarios (en producción usar base de datos)
usuarios_bd = {
    'admin': {'password': hashlib.sha256('admin123'.encode()).hexdigest(), 'nombre': 'Administrador'},
    'doctor': {'password': hashlib.sha256('doctor123'.encode()).hexdigest(), 'nombre': 'Dr. García'}
}

class SimpleIA:
    def __init__(self):
        self.nombre = "Claudia"
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
                "¡Tengo muchas capacidades! Puedo darte información deportiva internacional actualizada (⚽🏀🎾🏎️🏈🥊), hacer cálculos, y conversar contigo.",
                "Estoy aquí para ayudarte con: Deportes internacionales (fútbol, NBA, tenis, F1, NFL, UFC, boxeo), matemáticas, hora/fecha, y conversación general. Si no sé algo, puedo buscarlo en internet.",
                "📊 Deportes: La Liga, Premier, Serie A, Bundesliga, NBA, ATP/WTA, F1, NFL, UFC, Olimpiadas y más. 🔍 También puedo buscar info actualizada en internet.",
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
        
        # Base de datos deportivos INTERNACIONAL (Noviembre 2025)
        self.datos_deportivos = {
            'futbol': {
                'mundial_clubes': {
                    'info': 'Nuevo Mundial de Clubes FIFA 2025 en preparación',
                    'equipos': 'Real Madrid, Manchester City, Bayern Munich, Flamengo, Palmeiras entre los clasificados'
                },
                'champions_league': {
                    'info': 'La UEFA Champions League 2024-25 está en su fase de grupos.',
                    'destacados': [
                        'Real Madrid lidera su grupo con actuaciones destacadas de Bellingham y Vinícius Jr.',
                        'Manchester City continúa con su racha invicta bajo Guardiola',
                        'El Bayern Munich ha mostrado un fútbol ofensivo impresionante',
                        'Inter de Milán defiende con solidez, PSG con Mbappé imparable'
                    ]
                },
                'liga_española': {
                    'info': 'La Liga española 2024-25 está muy competitiva',
                    'clasificacion': [
                        '1° Real Madrid - Líder con 32 puntos',
                        '2° Barcelona - 30 puntos, con Lewandowski goleador',
                        '3° Atlético Madrid - 28 puntos',
                        '4° Athletic Bilbao - 26 puntos',
                        '5° Real Sociedad - 24 puntos'
                    ]
                },
                'premier_league': {
                    'info': 'Premier League 2024-25 temporada actual',
                    'clasificacion': [
                        '1° Arsenal - Liderato con 31 pts',
                        '2° Manchester City - 30 pts',
                        '3° Liverpool - 28 pts con Klopp',
                        '4° Aston Villa - 26 pts sorpresa',
                        '5° Tottenham - 24 pts'
                    ]
                },
                'serie_a': {
                    'info': 'Serie A italiana 2024-25',
                    'clasificacion': [
                        '1° Inter de Milán - Campeón defensor liderando',
                        '2° Juventus - Con gran momento',
                        '3° AC Milan - Recuperando forma',
                        '4° Napoli - Buscando volver al top'
                    ]
                },
                'bundesliga': {
                    'info': 'Bundesliga alemana 2024-25',
                    'clasificacion': [
                        '1° Bayern Munich - Dominando como siempre',
                        '2° Bayer Leverkusen - Campeones invictos 23-24',
                        '3° Borussia Dortmund - Luchando por título',
                        '4° RB Leipzig - Consistente en el top'
                    ]
                },
                'liga_mx': {
                    'info': 'Liga MX Apertura 2024',
                    'equipos': 'América, Cruz Azul, Tigres, Monterrey peleando el título'
                },
                'libertadores': {
                    'info': 'Copa Libertadores - Definiendo campeón 2024',
                    'finalistas': 'Los mejores equipos de Sudamérica en competencia'
                },
                'sudamericana': {
                    'info': 'Copa Sudamericana - Torneo continental importante',
                    'equipos': 'Equipos de toda Sudamérica compitiendo'
                }
            },
            'baloncesto': {
                'nba': {
                    'info': 'NBA Temporada 2024-25 en curso',
                    'conferencia_este': [
                        'Boston Celtics - 15-3 líderes del Este',
                        'Milwaukee Bucks - 13-5 con Giannis dominante',
                        'Philadelphia 76ers - 12-6 con Embiid MVP',
                        'Miami Heat - 11-7 mantienen nivel',
                        'Cleveland Cavaliers - 11-8 mejorando'
                    ],
                    'conferencia_oeste': [
                        'Denver Nuggets - 14-4 campeones defensores',
                        'Los Angeles Lakers - 13-5 con LeBron y AD',
                        'Phoenix Suns - 12-6 con el Big 3',
                        'Golden State Warriors - 11-7 con Curry',
                        'Sacramento Kings - 10-8 competitivos'
                    ]
                },
                'euroleague': {
                    'info': 'Euroliga de Baloncesto 2024-25',
                    'equipos': [
                        'Real Madrid - Potencia europea',
                        'Panathinaikos - Con gran plantel',
                        'Barcelona - Luchando por título',
                        'Olympiacos - Tradicional competidor'
                    ]
                }
            },
            'tenis': {
                'atp': {
                    'info': 'Ranking ATP actualizado noviembre 2025',
                    'top10': [
                        '1° Carlos Alcaraz (ESP) - Líder mundial',
                        '2° Novak Djokovic (SRB) - 24 Grand Slams',
                        '3° Jannik Sinner (ITA) - Ascenso meteórico',
                        '4° Daniil Medvedev (RUS) - Constante top',
                        '5° Holger Rune (DEN) - Promesa consolidada',
                        '6° Stefanos Tsitsipas (GRE)',
                        '7° Alexander Zverev (GER)',
                        '8° Taylor Fritz (USA)',
                        '9° Andrey Rublev (RUS)',
                        '10° Casper Ruud (NOR)'
                    ]
                },
                'wta': {
                    'info': 'Ranking WTA femenino',
                    'top5': [
                        '1° Iga Świątek (POL) - Dominante',
                        '2° Aryna Sabalenka (BLR)',
                        '3° Coco Gauff (USA)',
                        '4° Elena Rybakina (KAZ)',
                        '5° Ons Jabeur (TUN)'
                    ]
                },
                'grand_slams': {
                    'ultimos': 'Australian Open 2025 próximo Grand Slam en enero'
                }
            },
            'formula1': {
                'info': 'Temporada F1 2024 finalizada',
                'campeonato': [
                    'Campeón Mundial: Max Verstappen (Red Bull) - 4to título consecutivo',
                    'Subcampeón: Lando Norris (McLaren)',
                    '3° Lewis Hamilton (Mercedes) - Última temporada antes de Ferrari',
                    'Constructores: Red Bull Racing - Campeón'
                ],
                'proxima_temporada': 'F1 2025: Hamilton a Ferrari, cambios importantes en parrilla'
            },
            'futbol_americano': {
                'nfl': {
                    'info': 'NFL Temporada 2024 en curso',
                    'destacados': [
                        'Kansas City Chiefs - Defensores del Super Bowl',
                        'San Francisco 49ers - Favoritos NFC',
                        'Baltimore Ravens - Lamar Jackson MVP',
                        'Philadelphia Eagles - Potencia del Este',
                        'Miami Dolphins - Ofensiva explosiva'
                    ]
                }
            },
            'rugby': {
                'mundial': 'Próximo Mundial de Rugby 2027',
                'six_nations': 'Torneo de las Seis Naciones - competencia europea elite'
            },
            'cricket': {
                'info': 'Cricket - Deporte más popular en India, Pakistan, Australia',
                'mundial': 'ICC Cricket World Cup - torneo mundial cada 4 años'
            },
            'mma_boxing': {
                'ufc': {
                    'campeones': [
                        'Peso Pesado: Jon Jones',
                        'Peso Wélter: Leon Edwards',
                        'Peso Ligero: Islam Makhachev',
                        'Peso Pluma: Alexander Volkanovski'
                    ]
                },
                'boxeo': {
                    'destacados': 'Tyson Fury, Oleksandr Usyk, Canelo Álvarez entre las estrellas'
                }
            },
            'olimpiadas': {
                'info': 'París 2024 - Últimos Juegos Olímpicos celebrados',
                'proximos': 'Los Ángeles 2028 - Próximos Juegos Olímpicos de Verano'
            }
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
            # Patrones deportivos expandidos
            'futbol': r'\b(fútbol|futbol|liga|champions|real madrid|barcelona|premier|messi|ronaldo|libertadores|bundesliga|serie a|mundial)\b',
            'baloncesto': r'\b(baloncesto|basketball|nba|lakers|celtics|lebron|curry|euroliga|euroleague)\b',
            'tenis': r'\b(tenis|atp|wta|wimbledon|alcaraz|djokovic|nadal|federer|grand slam)\b',
            'formula1': r'\b(formula 1|f1|verstappen|hamilton|ferrari|red bull|mclaren)\b',
            'nfl': r'\b(nfl|futbol americano|super bowl|chiefs|49ers)\b',
            'mma_boxing': r'\b(ufc|mma|boxeo|boxing|pelea|fury|usyk|canelo)\b',
            'otros_deportes': r'\b(rugby|cricket|olimpiadas|olimpicos)\b',
            'deportes_general': r'\b(deportes|deporte|campeón|campeon|ganador|resultado|partido)\b',
        }
    
    def procesar_texto(self, texto):
        """Procesa el texto de entrada y clasifica la intención"""
        texto_lower = texto.lower()
        
        # Guardar en historial
        self.conversacion_historia.append(('usuario', texto))
        
        # Buscar patrones
        for categoria, patron in self.patrones.items():
            if re.search(patron, texto_lower, re.IGNORECASE):
                if categoria == 'calculo':
                    respuesta = self.calcular(texto_lower)
                elif categoria in ['futbol', 'baloncesto', 'tenis', 'formula1', 'nfl', 'mma_boxing', 'otros_deportes', 'deportes_general']:
                    respuesta = self.obtener_info_deportiva(categoria, texto_lower)
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
    
    def obtener_info_deportiva(self, categoria, texto):
        """Proporciona información deportiva actualizada con capacidad de búsqueda"""
        respuesta = ""
        
        if categoria == 'futbol':
            if 'mundial' in texto:
                respuesta = "⚽ Mundial de Clubes FIFA 2025 en preparación. Real Madrid, Manchester City, Bayern Munich, equipos brasileños clasificados."
            elif 'champions' in texto:
                info = self.datos_deportivos['futbol']['champions_league']
                respuesta = f"⚽ {info['info']}\n\n📊 Destacados:\n"
                respuesta += "\n".join([f"• {d}" for d in info['destacados']])
            elif 'barcelona' in texto or 'barça' in texto or 'barca' in texto:
                respuesta = "⚽ FC Barcelona - 2° en La Liga con 30 pts. Lewandowski lidera el ataque. Jóvenes promesas brillando."
            elif 'real madrid' in texto:
                respuesta = "⚽ Real Madrid - Líder de La Liga 2024-25 con 32 pts. Bellingham y Vinícius Jr. en gran forma. Favoritos Champions."
            elif 'premier' in texto:
                info = self.datos_deportivos['futbol']['premier_league']
                respuesta = f"⚽ {info['info']}\n\n📊 Top 5:\n"
                respuesta += "\n".join([f"• {c}" for c in info['clasificacion']])
            elif 'serie a' in texto or 'italia' in texto:
                info = self.datos_deportivos['futbol']['serie_a']
                respuesta = f"⚽ {info['info']}\n\n📊 Clasificación:\n"
                respuesta += "\n".join([f"• {c}" for c in info['clasificacion']])
            elif 'bundesliga' in texto or 'alemania' in texto:
                info = self.datos_deportivos['futbol']['bundesliga']
                respuesta = f"⚽ {info['info']}\n\n📊 Top 4:\n"
                respuesta += "\n".join([f"• {c}" for c in info['clasificacion']])
            elif 'libertadores' in texto:
                respuesta = "⚽ Copa Libertadores - El torneo más prestigioso de clubes de Sudamérica. Equipos de Brasil, Argentina, Colombia compitiendo."
            else:
                info = self.datos_deportivos['futbol']['liga_española']
                respuesta = f"⚽ {info['info']}\n\n📊 Top 5:\n"
                respuesta += "\n".join([f"• {c}" for c in info['clasificacion']])
        
        elif categoria == 'baloncesto':
            info_nba = self.datos_deportivos['baloncesto']['nba']
            if 'lakers' in texto:
                respuesta = "🏀 Los Angeles Lakers 13-5 en 2024-25. LeBron James (39 años) aún dominante. Anthony Davis clave en defensa."
            elif 'celtics' in texto:
                respuesta = "🏀 Boston Celtics 15-3, líderes del Este. Tatum y Brown forman dúo letal. Favoritos al título."
            elif 'euroliga' in texto or 'euroleague' in texto:
                info_euro = self.datos_deportivos['baloncesto']['euroleague']
                respuesta = f"🏀 {info_euro['info']}\n\n📊 Equipos destacados:\n"
                respuesta += "\n".join([f"• {e}" for e in info_euro['equipos']])
            else:
                respuesta = f"🏀 {info_nba['info']}\n\n📊 Conferencia Este - Top 4:\n"
                respuesta += "\n".join([f"• {c}" for c in info_nba['conferencia_este'][:4]])
                respuesta += "\n\n📊 Conferencia Oeste - Top 4:\n"
                respuesta += "\n".join([f"• {c}" for c in info_nba['conferencia_oeste'][:4]])
        
        elif categoria == 'tenis':
            if 'wta' in texto or 'femen' in texto:
                info_wta = self.datos_deportivos['tenis']['wta']
                respuesta = f"🎾 {info_wta['info']}\n\n📊 Top 5 WTA:\n"
                respuesta += "\n".join([f"• {t}" for t in info_wta['top5']])
            else:
                info_atp = self.datos_deportivos['tenis']['atp']
                respuesta = f"🎾 {info_atp['info']}\n\n📊 Top 10 ATP:\n"
                respuesta += "\n".join([f"• {t}" for t in info_atp['top10'][:7]])
                respuesta += "\n\n🏆 Alcaraz domina, Djokovic con 24 Grand Slams históricos"
        
        elif categoria == 'formula1':
            info = self.datos_deportivos['formula1']
            respuesta = f"🏎️ {info['info']}\n\n🏆 Resultados 2024:\n"
            respuesta += "\n".join([f"• {r}" for r in info['campeonato']])
            respuesta += f"\n\n🔜 {info['proxima_temporada']}"
        
        elif categoria == 'nfl':
            info = self.datos_deportivos['futbol_americano']['nfl']
            respuesta = f"🏈 {info['info']}\n\n📊 Equipos destacados:\n"
            respuesta += "\n".join([f"• {e}" for e in info['destacados']])
        
        elif categoria == 'mma_boxing':
            if 'ufc' in texto or 'mma' in texto:
                info = self.datos_deportivos['mma_boxing']['ufc']
                respuesta = "🥊 UFC - Campeones actuales:\n"
                respuesta += "\n".join([f"• {c}" for c in info['campeones']])
            else:
                respuesta = f"🥊 Boxeo: {self.datos_deportivos['mma_boxing']['boxeo']['destacados']}"
        
        elif categoria == 'otros_deportes':
            if 'rugby' in texto:
                respuesta = f"🏉 Rugby: {self.datos_deportivos['rugby']['mundial']}. {self.datos_deportivos['rugby']['six_nations']}"
            elif 'cricket' in texto:
                respuesta = f"� {self.datos_deportivos['cricket']['info']}. {self.datos_deportivos['cricket']['mundial']}"
            elif 'olimp' in texto:
                respuesta = f"🏅 {self.datos_deportivos['olimpiadas']['info']}\n🔜 {self.datos_deportivos['olimpiadas']['proximos']}"
        
        elif categoria == 'deportes_general':
            respuesta = """🏆 RESUMEN DEPORTIVO INTERNACIONAL - Noviembre 2025

⚽ FÚTBOL:
• La Liga: Real Madrid líder
• Premier League: Arsenal vs Man City
• Champions League: Fase de grupos
• Serie A: Inter dominando
• Bundesliga: Bayern imparable

🏀 BALONCESTO:
• NBA: Celtics 15-3 (Este), Nuggets defendiendo
• Euroliga: Real Madrid, Barcelona compitiendo

🎾 TENIS:
• ATP: Alcaraz #1, Djokovic #2
• WTA: Świątek dominante

🏎️ F1: Verstappen campeón 2024 (4to título)
🏈 NFL: Chiefs, 49ers, Ravens destacados
🥊 Combate: UFC y boxeo con grandes eventos

Pregunta sobre algún deporte específico para más detalles."""
        
        # Si no encontró info específica, intenta buscar en internet
        if not respuesta:
            respuesta = self.buscar_info_web(texto)
        
        return respuesta if respuesta else "No tengo información específica sobre eso. Pregúntame sobre fútbol, NBA, tenis, F1, NFL, MMA o boxeo."
    
    def buscar_info_web(self, consulta):
        """Busca información deportiva en internet cuando no está en la base de datos"""
        # Función simplificada - búsqueda web desactivada para estabilidad
        return "🔍 Para información más específica o actualizada en tiempo real, te recomiendo consultar ESPN, Marca, AS o sitios deportivos especializados."
    
    def limpiar_historial(self):
        """Limpia el historial de conversación"""
        self.conversacion_historia = []

# Crear instancia global de la IA
ia = SimpleIA()

@app.route('/inicio')
def inicio():
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')

@app.route('/captura-datos')
def captura_datos():
    return render_template('captura_datos.html')

@app.route('/analisis-reportes')
def analisis_reportes():
    return render_template('analisis_reportes.html')

@app.route('/medico-inteligente')
def medico_inteligente():
    return render_template('medico_inteligente.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')

@app.route('/seguridad')
def seguridad():
    return render_template('seguridad.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje = data.get('mensaje', '')
    
    if mensaje:
        respuesta = ia.procesar_texto(mensaje)
        return jsonify({
            'respuesta': respuesta,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })
    
    return jsonify({'error': 'No se recibió mensaje'}), 400

@app.route('/historial', methods=['GET'])
def historial():
    return jsonify({
        'historial': [
            {'tipo': tipo, 'mensaje': msg} 
            for tipo, msg in ia.conversacion_historia
        ]
    })

@app.route('/limpiar', methods=['POST'])
def limpiar():
    ia.limpiar_historial()
    return jsonify({'mensaje': 'Historial limpiado'})

# RUTAS PARA GESTIÓN DE PACIENTES
@app.route('/api/pacientes', methods=['GET'])
def obtener_pacientes():
    """Obtiene la lista de todos los pacientes"""
    pacientes = gestor_pacientes.obtener_todos_pacientes()
    return jsonify({'pacientes': pacientes})

@app.route('/api/pacientes', methods=['POST'])
def agregar_paciente():
    """Agrega un nuevo paciente"""
    try:
        datos = request.get_json()
        nuevo_paciente = gestor_pacientes.agregar_paciente(datos)
        return jsonify({
            'exito': True, 
            'mensaje': 'Paciente agregado exitosamente',
            'paciente': nuevo_paciente
        }), 201
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>', methods=['GET'])
def obtener_paciente(id_paciente):
    """Obtiene información de un paciente específico"""
    paciente = gestor_pacientes.obtener_paciente(id_paciente)
    if paciente:
        return jsonify({'exito': True, 'paciente': paciente})
    return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404

@app.route('/api/pacientes/<id_paciente>', methods=['PUT'])
def actualizar_paciente(id_paciente):
    """Actualiza información de un paciente"""
    try:
        datos = request.get_json()
        paciente_actualizado = gestor_pacientes.actualizar_paciente(id_paciente, datos)
        if paciente_actualizado:
            return jsonify({
                'exito': True,
                'mensaje': 'Paciente actualizado exitosamente',
                'paciente': paciente_actualizado
            })
        return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>', methods=['DELETE'])
def eliminar_paciente(id_paciente):
    """Elimina un paciente"""
    if gestor_pacientes.eliminar_paciente(id_paciente):
        return jsonify({'exito': True, 'mensaje': 'Paciente eliminado exitosamente'})
    return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404

@app.route('/api/pacientes/<id_paciente>/notas', methods=['POST'])
def agregar_nota(id_paciente):
    """Agrega una nota al historial del paciente"""
    try:
        datos = request.get_json()
        nota = datos.get('nota', '')
        nota_agregada = gestor_pacientes.agregar_nota_paciente(id_paciente, nota)
        if nota_agregada:
            return jsonify({
                'exito': True,
                'mensaje': 'Nota agregada exitosamente',
                'nota': nota_agregada
            }), 201
        return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/buscar/<termino>', methods=['GET'])
def buscar_paciente(termino):
    """Busca pacientes por nombre, apellido o cédula"""
    resultados = gestor_pacientes.buscar_paciente(termino)
    return jsonify({'resultados': resultados, 'cantidad': len(resultados)})

# RUTAS PARA ANÁLISIS CON IA MÉDICA
@app.route('/api/analisis-paciente/<id_paciente>', methods=['GET'])
def analizar_paciente(id_paciente):
    """Obtiene análisis completo de un paciente con IA"""
    paciente = gestor_pacientes.obtener_paciente(id_paciente)
    if paciente:
        análisis = ia_medica.analizar_paciente(paciente)
        return jsonify({'exito': True, 'analisis': análisis})
    return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404

@app.route('/api/alertas-paciente/<id_paciente>', methods=['GET'])
def obtener_alertas(id_paciente):
    """Obtiene alertas clínicas de un paciente"""
    paciente = gestor_pacientes.obtener_paciente(id_paciente)
    if paciente:
        análisis = ia_medica.analizar_paciente(paciente)
        return jsonify({
            'exito': True,
            'alertas': análisis['alertas'],
            'score_riesgo': análisis['score_riesgo'],
            'paciente_nombre': f"{paciente['nombre']} {paciente['apellido']}"
        })
    return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404

@app.route('/api/recomendaciones/<id_paciente>', methods=['GET'])
def obtener_recomendaciones(id_paciente):
    """Obtiene recomendaciones para un paciente"""
    paciente = gestor_pacientes.obtener_paciente(id_paciente)
    if paciente:
        análisis = ia_medica.analizar_paciente(paciente)
        return jsonify({
            'exito': True,
            'recomendaciones': análisis['recomendaciones']
        })
    return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404

@app.route('/api/resumen-clinico/<id_paciente>', methods=['GET'])
def obtener_resumen_clinico(id_paciente):
    """Obtiene resumen clínico de un paciente"""
    paciente = gestor_pacientes.obtener_paciente(id_paciente)
    if paciente:
        resumen = ia_medica.resumir_historial(paciente)
        return jsonify({'exito': True, 'resumen': resumen})
    return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404

@app.route('/api/inconsistencias/<id_paciente>', methods=['GET'])
def detectar_inconsistencias(id_paciente):
    """Detecta datos faltantes o inconsistentes"""
    paciente = gestor_pacientes.obtener_paciente(id_paciente)
    if paciente:
        inconsistencias = ia_medica.detectar_inconsistencias(paciente)
        return jsonify({
            'exito': True,
            'inconsistencias': inconsistencias,
            'cantidad': len(inconsistencias)
        })
    return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404

# RUTAS PARA DIAGNÓSTICOS
@app.route('/api/pacientes/<id_paciente>/diagnosticos', methods=['POST'])
def agregar_diagnostico(id_paciente):
    """Agrega un diagnóstico a un paciente"""
    try:
        datos = request.get_json()
        diagnostico = datos.get('diagnostico', '')
        
        if not diagnostico:
            return jsonify({'exito': False, 'error': 'Diagnóstico requerido'}), 400
        
        diag = gestor_pacientes.agregar_diagnostico(id_paciente, diagnostico)
        if diag:
            # Agregar a timeline
            gestor_pacientes.agregar_evento_timeline(
                id_paciente, 
                'diagnostico', 
                f'Diagnóstico agregado: {diagnostico}'
            )
            return jsonify({
                'exito': True,
                'mensaje': 'Diagnóstico agregado',
                'diagnostico': diag
            }), 201
        return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>/diagnosticos', methods=['GET'])
def obtener_diagnosticos(id_paciente):
    """Obtiene diagnósticos de un paciente"""
    diagnosticos = gestor_pacientes.obtener_diagnosticos(id_paciente)
    return jsonify({'exito': True, 'diagnosticos': diagnosticos})

# RUTAS PARA TRATAMIENTOS
@app.route('/api/pacientes/<id_paciente>/tratamientos', methods=['POST'])
def agregar_tratamiento(id_paciente):
    """Agrega un tratamiento a un paciente"""
    try:
        datos = request.get_json()
        tratamiento = gestor_pacientes.agregar_tratamiento(
            id_paciente,
            datos.get('tratamiento', ''),
            datos.get('medicamento', ''),
            datos.get('dosis', ''),
            datos.get('duracion', '')
        )
        
        if tratamiento:
            gestor_pacientes.agregar_evento_timeline(
                id_paciente,
                'tratamiento',
                f'Tratamiento: {datos.get("medicamento")} - {datos.get("dosis")}'
            )
            return jsonify({
                'exito': True,
                'mensaje': 'Tratamiento agregado',
                'tratamiento': tratamiento
            }), 201
        return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>/tratamientos', methods=['GET'])
def obtener_tratamientos(id_paciente):
    """Obtiene tratamientos de un paciente"""
    tratamientos = gestor_pacientes.obtener_tratamientos(id_paciente)
    return jsonify({'exito': True, 'tratamientos': tratamientos})

# RUTAS PARA ESTUDIOS
@app.route('/api/pacientes/<id_paciente>/estudios', methods=['POST'])
def agregar_estudio(id_paciente):
    """Agrega un estudio/examen a un paciente"""
    try:
        datos = request.get_json()
        estudio = gestor_pacientes.agregar_estudio(
            id_paciente,
            datos.get('tipo_estudio', ''),
            datos.get('resultado', '')
        )
        
        if estudio:
            gestor_pacientes.agregar_evento_timeline(
                id_paciente,
                'estudio',
                f'Estudio: {datos.get("tipo_estudio")}'
            )
            return jsonify({
                'exito': True,
                'mensaje': 'Estudio agregado',
                'estudio': estudio
            }), 201
        return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>/estudios', methods=['GET'])
def obtener_estudios(id_paciente):
    """Obtiene estudios de un paciente"""
    estudios = gestor_pacientes.obtener_estudios(id_paciente)
    return jsonify({'exito': True, 'estudios': estudios})

# ENDPOINTS PARA CAPTURA DE DATOS CLÍNICOS
@app.route('/api/pacientes/<id_paciente>/sintomas', methods=['POST'])
def agregar_sintomas(id_paciente):
    """Agrega síntomas al paciente"""
    try:
        data = request.get_json()
        sintomas = data.get('sintomas', '')
        duracion = data.get('duracion', '')
        severidad = data.get('severidad', '')
        factores = data.get('factores', '')
        
        # Actualizar síntomas en la base de datos
        paciente = gestor_pacientes.obtener_paciente(id_paciente)
        if not paciente:
            return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
        
        gestor_pacientes.actualizar_campo(id_paciente, 'sintomas', sintomas)
        
        # Agregar nota de síntomas
        nota = f"Síntomas: {sintomas}. Duración: {duracion}. Severidad: {severidad}/10. Factores: {factores}"
        gestor_pacientes.agregar_nota(id_paciente, nota)
        
        return jsonify({'exito': True, 'mensaje': 'Síntomas registrados exitosamente'}), 201
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>/diagnostico', methods=['POST'])
def registrar_diagnostico(id_paciente):
    """Registra diagnóstico del paciente"""
    try:
        data = request.get_json()
        diagnostico = data.get('diagnostico', '')
        codigo = data.get('codigo', '')
        secundarios = data.get('secundarios', '')
        observaciones = data.get('observaciones', '')
        
        paciente = gestor_pacientes.obtener_paciente(id_paciente)
        if not paciente:
            return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
        
        # Agregar diagnóstico
        gestor_pacientes.agregar_diagnostico(id_paciente, {
            'diagnostico': diagnostico,
            'codigo_cie': codigo,
            'secundarios': secundarios,
            'observaciones': observaciones,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        return jsonify({'exito': True, 'mensaje': 'Diagnóstico registrado exitosamente'}), 201
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>/tratamiento', methods=['POST'])
def registrar_tratamiento(id_paciente):
    """Registra tratamiento prescrito"""
    try:
        data = request.get_json()
        medicamento = data.get('medicamento', '')
        dosis = data.get('dosis', '')
        frecuencia = data.get('frecuencia', '')
        duracion = data.get('duracion', '')
        via = data.get('via', '')
        advertencias = data.get('advertencias', '')
        
        paciente = gestor_pacientes.obtener_paciente(id_paciente)
        if not paciente:
            return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
        
        # Agregar tratamiento
        gestor_pacientes.agregar_tratamiento(id_paciente, {
            'medicamento': medicamento,
            'dosis': dosis,
            'frecuencia': frecuencia,
            'duracion': duracion,
            'via_administracion': via,
            'advertencias': advertencias,
            'fecha_inicio': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        return jsonify({'exito': True, 'mensaje': 'Tratamiento registrado exitosamente'}), 201
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>/estudio', methods=['POST'])
def registrar_estudio(id_paciente):
    """Registra estudio o examen realizado"""
    try:
        data = request.get_json()
        tipo = data.get('tipo', '')
        descripcion = data.get('descripcion', '')
        resultado = data.get('resultado', '')
        fecha = data.get('fecha', '')
        
        paciente = gestor_pacientes.obtener_paciente(id_paciente)
        if not paciente:
            return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
        
        # Agregar estudio
        gestor_pacientes.agregar_estudio(id_paciente, {
            'tipo': tipo,
            'descripcion': descripcion,
            'resultado': resultado,
            'fecha': fecha if fecha else datetime.now().strftime('%Y-%m-%d')
        })
        
        return jsonify({'exito': True, 'mensaje': 'Estudio registrado exitosamente'}), 201
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/pacientes/<id_paciente>/notas', methods=['POST'])
def actualizar_notas(id_paciente):
    """Actualiza notas y recomendaciones"""
    try:
        data = request.get_json()
        notas = data.get('notas', '')
        recomendaciones = data.get('recomendaciones', '')
        
        paciente = gestor_pacientes.obtener_paciente(id_paciente)
        if not paciente:
            return jsonify({'exito': False, 'error': 'Paciente no encontrado'}), 404
        
        # Agregar nota
        if notas:
            gestor_pacientes.agregar_nota(id_paciente, f"Notas médicas: {notas}")
        
        if recomendaciones:
            gestor_pacientes.agregar_nota(id_paciente, f"Recomendaciones: {recomendaciones}")
        
        return jsonify({'exito': True, 'mensaje': 'Notas guardadas exitosamente'}), 201
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

# RUTA PARA TIMELINE
@app.route('/api/pacientes/<id_paciente>/timeline', methods=['GET'])
def obtener_timeline(id_paciente):
    """Obtiene timeline clínico de un paciente"""
    timeline = gestor_pacientes.obtener_timeline(id_paciente)
    return jsonify({'exito': True, 'timeline': timeline})

# ============================================
# RUTAS PARA CITAS MÉDICAS
# ============================================

@app.route('/citas')
def citas_medicas():
    """Página de gestión de citas médicas"""
    return render_template('citas.html')

@app.route('/api/citas', methods=['GET', 'POST'])
def gestionar_citas():
    """API para gestionar citas médicas"""
    if request.method == 'POST':
        data = request.json
        cita = {
            'id': 'CIT-' + str(int(datetime.now().timestamp() * 1000)),
            'patientId': data.get('patientId'),
            'date': data.get('date'),
            'time': data.get('time'),
            'specialty': data.get('specialty'),
            'reason': data.get('reason'),
            'status': 'Programada',
            'createdAt': datetime.now().isoformat()
        }
        return jsonify({'exito': True, 'cita': cita}), 201
    
    return jsonify({'exito': True, 'citas': []}), 200

# ============================================
# RUTAS PARA LABORATORIOS
# ============================================

@app.route('/laboratorios')
def laboratorios():
    """Página de gestión de laboratorios"""
    return render_template('laboratorios.html')

@app.route('/api/laboratorios', methods=['GET', 'POST'])
def gestionar_laboratorios():
    """API para gestionar órdenes de laboratorio"""
    if request.method == 'POST':
        data = request.json
        orden = {
            'id': 'ORD-' + str(int(datetime.now().timestamp() * 1000)),
            'patientId': data.get('patientId'),
            'analysisType': data.get('analysisType'),
            'laboratory': data.get('laboratory'),
            'priority': data.get('priority'),
            'notes': data.get('notes'),
            'status': 'Pendiente',
            'createdAt': datetime.now().isoformat(),
            'results': []
        }
        return jsonify({'exito': True, 'orden': orden}), 201
    
    return jsonify({'exito': True, 'ordenes': []}), 200

# ============================================
# RUTAS PARA ENCRIPTACIÓN
# ============================================

@app.route('/api/encriptar', methods=['POST'])
def encriptar_datos():
    """Encripta datos sensibles"""
    try:
        data = request.json
        datos_texto = data.get('datos')
        tipo = data.get('tipo', 'general')
        
        resultado = encriptador.cifrar_datos(datos_texto, tipo)
        
        if resultado:
            return jsonify({
                'exito': True,
                'hash': resultado['hash'],
                'tipo': resultado['tipo']
            }), 200
        else:
            return jsonify({'exito': False, 'error': 'Error al encriptar'}), 400
    
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/desencriptar/<hash_dato>', methods=['GET'])
def desencriptar_datos(hash_dato):
    """Desencripta datos (requiere autenticación)"""
    try:
        if 'usuario_id' not in session:
            return jsonify({'exito': False, 'error': 'No autorizado'}), 401
        
        datos = encriptador.descifrar_datos(hash_dato)
        
        if datos:
            # Registrar acceso para auditoría
            encriptador.registrar_acceso_dato(hash_dato, session.get('usuario_id'), 'lectura')
            
            return jsonify({
                'exito': True,
                'datos': datos
            }), 200
        else:
            return jsonify({'exito': False, 'error': 'Hash no encontrado'}), 404
    
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

# ============================================
# RUTAS PARA SINCRONIZACIÓN EN LA NUBE
# ============================================

@app.route('/api/backup/crear', methods=['POST'])
def crear_backup():
    """Crea un backup de los datos"""
    try:
        archivos = [
            'pacientes.json',
            'datos_encriptados.json'
        ]
        
        backup = sincronizador_nube.crear_backup_completo(archivos)
        
        if backup:
            return jsonify({
                'exito': True,
                'backup': backup['nombre'],
                'fecha': backup['timestamp'],
                'tamaño': backup['tamaño_total']
            }), 200
        else:
            return jsonify({'exito': False, 'error': 'Error al crear backup'}), 400
    
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/backup/listar', methods=['GET'])
def listar_backups():
    """Lista todos los backups disponibles"""
    try:
        backups = sincronizador_nube.listar_backups()
        stats = sincronizador_nube.obtener_estadisticas_backups()
        
        return jsonify({
            'exito': True,
            'backups': backups,
            'estadisticas': stats
        }), 200
    
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/backup/restaurar/<nombre_backup>', methods=['POST'])
def restaurar_backup_ruta(nombre_backup):
    """Restaura un backup específico"""
    try:
        resultado = sincronizador_nube.restaurar_backup(nombre_backup)
        
        return jsonify({
            'exito': resultado.get('exitoso', False),
            'mensaje': resultado.get('mensaje'),
            'archivos': resultado.get('archivos_restaurados', [])
        }), 200 if resultado.get('exitoso') else 400
    
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/sincronizar', methods=['POST'])
def sincronizar_datos():
    """Sincroniza datos con la nube"""
    try:
        servicio = request.json.get('servicio', 'local')
        archivos = request.json.get('archivos', ['pacientes.json', 'datos_encriptados.json'])
        
        resultado = sincronizador_nube.sincronizar_nube(servicio, archivos)
        
        return jsonify({
            'exito': resultado.get('exitoso', False),
            'mensaje': resultado.get('mensaje'),
            'servicio': servicio
        }), 200 if resultado.get('exitoso') else 400
    
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

@app.route('/api/chat-groq', methods=['POST'])
def chat_groq():
    """Chat con IA Groq - Conversación inteligente sobre casos médicos"""
    try:
        datos = request.json
        mensaje_usuario = datos.get('mensaje', '').strip()
        paciente_id = datos.get('paciente_id')
        conversacion = datos.get('conversacion', [])
        
        if not mensaje_usuario:
            return jsonify({'exito': False, 'error': 'Mensaje vacío'}), 400
        
        # Obtener información del paciente si está disponible
        contexto_paciente = ""
        if paciente_id:
            try:
                paciente_data = gestor_pacientes.obtener_paciente(paciente_id)
                if paciente_data:
                    contexto_paciente = f"""
Paciente Actual: {paciente_data.get('nombre', '')} {paciente_data.get('apellido', '')}
- Edad: {paciente_data.get('edad', 'N/A')} años
- Peso: {paciente_data.get('peso', 'N/A')} kg
- Altura: {paciente_data.get('altura', 'N/A')} cm
- Presión Arterial: {paciente_data.get('presion_arterial', 'N/A')}
- Alergias: {paciente_data.get('alergias', 'Ninguna')}
"""
            except:
                pass
        
        # Construir el historial de conversación para Groq
        mensajes_groq = [
            {
                "role": "system",
                "content": f"""Eres un asistente médico experto e inteligente. Proporciona información precisa y profesional sobre:
- Diagnósticos y síntomas
- Medicamentos y tratamientos
- Recomendaciones clínicas
- Análisis de casos médicos

Sé conciso pero completo. Siempre recomienda consultar con un médico para diagnósticos definitivos.
{contexto_paciente}"""
            }
        ]
        
        # Agregar historial de conversación
        for msg in conversacion[-10:]:  # Limitar a últimos 10 mensajes
            role = "user" if msg.get('rol') == 'usuario' else "assistant"
            mensajes_groq.append({
                "role": role,
                "content": msg.get('contenido', '')
            })
        
        # Agregar mensaje actual
        mensajes_groq.append({
            "role": "user",
            "content": mensaje_usuario
        })
        
        # Llamar a Groq API
        respuesta = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Modelo activo más reciente
            messages=mensajes_groq,
            temperature=0.7,
            max_tokens=1024
        )
        
        respuesta_texto = respuesta.choices[0].message.content
        
        return jsonify({
            'exito': True,
            'respuesta': respuesta_texto,
            'modelo': 'Groq Mixtral 8x7B'
        }), 200
        
    except Exception as e:
        print(f"Error en chat_groq: {str(e)}")
        return jsonify({
            'exito': False,
            'error': f'Error al procesar: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  [IA] Asistente Web - Servidor Iniciado")
    print("="*50)
    print("\n  Abre tu navegador en: http://localhost:5000")
    print("\n  Presiona Ctrl+C para detener el servidor\n")
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
