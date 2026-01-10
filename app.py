print("Hola desde app.py")
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
#from openai import OpenAI

#client = OpenAI(api_key="TU_API_KEY_AQUI")

app = Flask(__name__)
CORS(app)
#@app.route("/explicar", methods=["POST"])
#def explicar():
#    data = request.json

#    prompt = f"""
#El cliente cotizó un auto con estos datos:

#Marca: {data['marca']}
#Modelo: {data['modelo']}
#Año: {data['year']}
#Kilómetros: {data['km']}
# Estado: {data['estado']}

# Precio estimado: entre S/. {data['min']} y S/. {data['max']}

# Explícale de forma breve, clara y amigable por qué salió ese rango de precio,
# hablando de depreciación, kilometraje y estado del vehículo.
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "Eres un asesor de compra de autos en Perú."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=120
#     )

#     return jsonify({
#         "respuesta": response.choices[0].message.content
#     })
    
@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.json

    try:
        year = int(data["year"])
        km = int(data["km"])
        estado = data["estado"].lower()
    except:
        return jsonify({"error": "Datos inválidos"}), 400

    precio_base = 50000
    depreciacion_anual = (2025 - year) * 1500
    depreciacion_km = (km // 10000) * 800

    factor_estado = {
        "excelente": 1.0,
        "bueno": 0.9,
        "regular": 0.8
    }

    precio = (precio_base - depreciacion_anual - depreciacion_km) * factor_estado.get(estado, 0.85)

    return jsonify({
        "min": round(precio * 0.95),
        "max": round(precio * 1.05)
    })

if __name__ == "__main__":
    
    app.run(debug=True)
    
   