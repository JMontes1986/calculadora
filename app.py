from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random
import os
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Configurar Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def generar_problema(grade_band="2-3", previous=None):
    """Genera un nuevo problema matemático según el nivel"""
    
    # Configuración de rangos por nivel
    config = {
        "1-2": {"suma_max": 20, "mult_max": 5, "div_max": 10},
        "2-3": {"suma_max": 50, "mult_max": 10, "div_max": 10},
        "4-5": {"suma_max": 100, "mult_max": 12, "div_max": 12}
    }
    
    cfg = config.get(grade_band, config["2-3"])
    
    # Seleccionar operación
    operaciones = ["+", "-", "×", "÷"]
    op = random.choice(operaciones)
    
    # Evitar repetir operación si hay historial
    if previous and previous.get("op"):
        intentos = 0
        while op == previous["op"] and intentos < 3:
            op = random.choice(operaciones)
            intentos += 1
    
    # Generar números según operación
    if op == "+":
        a = random.randint(1, cfg["suma_max"])
        b = random.randint(1, cfg["suma_max"] - a)
        hint = f"Suma {a} más {b}. Puedes contar con los dedos o dibujar."
        explanation = f"Para sumar {a} + {b}, empieza en {a} y cuenta {b} números más: {a + b}."
        
    elif op == "-":
        a = random.randint(2, cfg["suma_max"])
        b = random.randint(1, a)
        hint = f"¿Cuánto queda si a {a} le quitas {b}?"
        explanation = f"Para restar {a} - {b}, cuenta hacia atrás desde {a}, {b} veces: {a - b}."
        
    elif op == "×":
        a = random.randint(2, cfg["mult_max"])
        b = random.randint(2, cfg["mult_max"])
        hint = f"Multiplica {a} por {b}. Piensa en {a} grupos de {b}."
        explanation = f"Para {a} × {b}, suma {b} veces: " + " + ".join([str(b)] * a) + f" = {a * b}."
        
    else:  # ÷
        b = random.randint(2, cfg["div_max"])
        resultado = random.randint(2, cfg["div_max"])
        a = b * resultado
        hint = f"¿Cuántas veces cabe {b} en {a}?"
        explanation = f"Divide {a} entre {b} contando de {b} en {b} hasta llegar a {a}. Son {resultado} veces."
    
    encouragements = [
        "¡Excelente trabajo!",
        "¡Muy bien!",
        "¡Sigue así!",
        "¡Lo estás haciendo genial!",
        "¡Eres muy bueno en esto!"
    ]
    
    return {
        "next_problem": {"a": a, "b": b, "op": op},
        "hint": hint,
        "encouragement": random.choice(encouragements),
        "explanation_if_wrong": explanation
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/problema', methods=['POST'])
def obtener_problema():
    """Endpoint para obtener un nuevo problema"""
    try:
        data = request.json or {}
        grade_band = data.get('gradeBand', '2-3')
        previous = data.get('previous')
        
        problema = generar_problema(grade_band, previous)
        
        # Guardar en Supabase si está configurado
        if supabase:
            try:
                supabase.table('problemas').insert({
                    'grade_band': grade_band,
                    'problema': problema['next_problem'],
                    'hint': problema['hint']
                }).execute()
            except:
                pass  # Continuar si falla el guardado
        
        return jsonify(problema)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/respuesta', methods=['POST'])
def verificar_respuesta():
    """Endpoint para verificar respuesta del estudiante"""
    try:
        data = request.json
        a = data['a']
        b = data['b']
        op = data['op']
        respuesta = data['respuesta']
        
        # Calcular respuesta correcta
        if op == '+':
            correcta = a + b
        elif op == '-':
            correcta = a - b
        elif op == '×':
            correcta = a * b
        else:  # ÷
            correcta = a // b
        
        es_correcta = respuesta == correcta
        
        # Guardar en Supabase si está configurado
        if supabase:
            try:
                supabase.table('respuestas').insert({
                    'problema': {'a': a, 'b': b, 'op': op},
                    'respuesta_usuario': respuesta,
                    'respuesta_correcta': correcta,
                    'es_correcta': es_correcta
                }).execute()
            except:
                pass
        
        return jsonify({
            "correcta": es_correcta,
            "respuesta_correcta": correcta
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
