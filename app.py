from flask import Flask, render_template, request
from pymongo import MongoClient

# Iniciar la aplicación web
app = Flask(__name__)

# 1. CREAR LA CONEXIÓN A MONGODB COMPASS
# Localhost y el puerto 27017 son los valores por defecto de MongoDB
cliente = MongoClient('mongodb://localhost:27017/')

# 2. SELECCIONAR LA BASE DE DATOS Y LAS COLECCIONES
db = cliente['prueba3'] # Asegúrate de que tu BD en Compass se llame así
coleccion_eventos = db['eventos']
coleccion_invitados = db['invitados']

# 3. CREAR LA RUTA PRINCIPAL (Listado de Eventos)


# 1. Inicio y Eventos
@app.route('/')
def mostrar_eventos():
    categoria_seleccionada = request.args.get('categoria')

    filtro = {}
    if categoria_seleccionada:
        filtro = {"categoria": categoria_seleccionada}

    campos_a_traer = {"codigo": 1, "nombre": 1, "fecha": 1, "lugar": 1, "categoria": 1, "_id": 0}
    
    eventos_db = list(coleccion_eventos.find(filtro, campos_a_traer))
    
    return render_template('eventos.html', lista_eventos=eventos_db)


@app.route('/eventos.html')
def mostrar_eventos_listado():
    categoria_seleccionada = request.args.get('categoria')

    filtro = {}
    if categoria_seleccionada:
        filtro = {"categoria": categoria_seleccionada}

    campos_a_traer = {"codigo": 1, "nombre": 1, "fecha": 1, "lugar": 1, "categoria": 1, "_id": 0}

    eventos_db = list(coleccion_eventos.find(filtro, campos_a_traer))

    return render_template('eventos.html', lista_eventos=eventos_db)

# 2. Ruta Búsqueda de Invitados
@app.route('/invitados.html')
def mostrar_invitados():
    return render_template('invitados.html')

# 3. Ruta Validación de Accesos
@app.route('/validacion.html')
def mostrar_validacion():
    return render_template('validacion.html')

# 4. Ruta Top 3
@app.route('/top.html')
def mostrar_top():
    return render_template('top.html')

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)