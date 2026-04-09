from flask import request, jsonify

def calcular():
    data = request.json
    resultado = calcular_logica(data)
    return jsonify(resultado)