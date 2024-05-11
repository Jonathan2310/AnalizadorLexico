from flask import Flask, request, jsonify
from flask_cors import CORS
import lexer
import logging

app = Flask(__name__)
CORS(app)
app.secret_key = 'clavee22'
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['POST'])
def index():
    if 'file' in request.files and request.is_json:
        return jsonify({'error': 'Se proporcionó tanto un archivo como datos JSON. Proporcione solo uno de ellos.'}), 400
    elif 'file' in request.files:
        file = request.files['file']
        codigo = file.read().decode('utf-8')
        logging.debug(f"Code from file: {codigo}")
    elif request.is_json:
        data = request.json
        codigo = data.get('textarea_content', '')
        logging.debug(f"Code from JSON: {codigo}")
    else:
        return jsonify({'error': 'No se proporcionó ningún archivo ni datos JSON'}), 400

    tokens = []
    lexer.lexer.input(codigo)
    line_number = 1
    while True:
        tok = lexer.lexer.token()
        if not tok:
            break
        if tok.type in lexer.reserved.values():
            token_type = f"<Reservada {tok.type.title()}>"
        elif tok.type == 'LPAREN':
            token_type = "<Paréntesis de apertura>"
        elif tok.type == 'RPAREN':
            token_type = "<Paréntesis de cierre>"
        else:
            token_type = tok.type
        tokens.append((f"Línea {line_number}", token_type, tok.value))
        logging.debug(f"Token: {tok}")
        line_number += 1

    return jsonify({'tokens': tokens})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
