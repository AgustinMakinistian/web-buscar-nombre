from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Cargar el archivo Excel
def load_data():
    return pd.read_excel('base_datos.xlsx')

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_data()  # Cargar los datos

    if request.method == "POST":
        # Obtener los valores de los campos de búsqueda
        name_query = request.form.get("name", "").strip().lower()
        brand_query = request.form.get("brand", "").strip().lower()
        vehicle_query = request.form.get("vehicle", "").strip().lower()

        # Filtrar el DataFrame según los criterios de búsqueda
        if name_query:
            df = df[df['Nombre'].str.contains(name_query, case=False, na=False)]
        if brand_query:
            df = df[df['Marca'].str.contains(brand_query, case=False, na=False)]
        if vehicle_query:
            df = df[df['Vehiculo'].str.contains(vehicle_query, case=False, na=False)]

        # Convertir a una lista de diccionarios para pasar al HTML
        data_dict = df.to_dict(orient='records')
        return render_template('index.html', data=data_dict)

    # Si no es una búsqueda, mostrar todos los datos
    return render_template('index.html', data=[])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
