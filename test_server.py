from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor funcionando!"

@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    return jsonify({'mensaje': 'Recibido: ' + data.get('texto', 'nada')})

if __name__ == '__main__':
    print("Servidor de prueba iniciado")
    app.run(debug=True, host='0.0.0.0', port=5001)
