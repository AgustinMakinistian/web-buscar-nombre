from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Cargar el archivo Excel
def load_data():
    return pd.read_excel('base_datos.xlsx')

@app.route("/", methods=["GET", "POST"])
def index():
    # Cargar el archivo de datos solo una vez
    df = load_data()

    # Si se recibe una búsqueda
    if request.method == "POST":
        search_query = request.form.get("search", "").strip().lower()

        # Verificar si la columna 'Nombre' contiene valores nulos y reemplazarlos por una cadena vacía
        df['Nombre'] = df['Nombre'].fillna('')

        # Buscar en la columna 'Nombre' si contiene el término de búsqueda (ignorando mayúsculas/minúsculas)
        if search_query:
            data = df[df['Nombre'].str.contains(search_query, case=False, na=False)]
        else:
            data = df  # Si no hay búsqueda, mostrar todos los datos

        # Convertir el DataFrame en una lista de diccionarios
        data_dict = data.to_dict(orient='records')

        return render_template('index.html', data=data_dict)

    # Si no es una búsqueda, mostrar todos los datos
    return render_template('index.html', data=[])

if __name__ == "__main__":
    # Cambiar a un puerto dinámico proporcionado por el entorno de Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
