from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/")
def index():
    return render_template("service.html")
@app.route("/cotizar", methods=["POST"])
def cotizar():
    data = request.json
    year = data.get("year")
    brand = data.get("brand")
    model = data.get("model")
    
    # Lógica de cotización simulada
    precio_base= 20000
    if year and year.isdigit():
        antiguedad = 2025 - int(year)
        precio_base -= antiguedad * 500

    return jsonify({
        "ok": True,
        "precio_estimado": precio_base,
        "mensaje": f"Tu {brand} {model} del {year} tiene un precio estimado de ${precio_base}"        
    })
    
if __name__ == "__main__":
    app.run(debug=True)


# Precios base simulados
PRECIOS_BASE = {
    ("toyota", "corolla"): 45000,
    ("toyota", "hilux"): 80000,
    ("nissan", "sentra"): 42000
}

@app.route("/tasar", methods=["POST"])
def tasar_auto():
    data = request.json

    marca = data["marca"].lower()
    modelo = data["modelo"].lower()
    anio = int(data["anio"])
    km = int(data["km"])
    estado = data["estado"]

    precio_base = PRECIOS_BASE.get((marca, modelo), 40000)

    # Depreciación por año
    antiguedad = 2025 - anio
    precio = precio_base * (1 - 0.05 * antiguedad)

    # Depreciación por kilometraje
    km_extra = max(0, km - 20000 * antiguedad)
    precio -= km_extra * 0.05

    # Ajuste por estado
    if estado == "excelente":
        precio *= 1.05
    elif estado == "regular":
        precio *= 0.9

    precio_min = round(precio * 0.95)
    precio_max = round(precio * 1.05)

    return jsonify({
        "precio_min": precio_min,
        "precio_max": precio_max
    })

if __name__ == "__main__":
    app.run(debug=True)