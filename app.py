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
    patron_busqueda = request.args.get('busqueda')

    filtro = {}

    if patron_busqueda:
        patron_busqueda = f".*{patron_busqueda}.*" 
        filtro = {
            "$or": [
                {"nombre": {"$regex": patron_busqueda, "$options": "i"}},
                {"apellido": {"$regex": patron_busqueda, "$options": "i"}},
                {"correo": {"$regex": patron_busqueda, "$options": "i"}},
                {"estado": {"$regex": patron_busqueda, "$options": "i"}},
                {"rut": {"$regex": patron_busqueda, "$options": "i"}}
            ]
        }

    invitados_db = list(coleccion_invitados.find(filtro))
    return render_template('invitados.html', lista_invitados=invitados_db)

# 3. Ruta Validación de Accesos
@app.route('/validacion.html')
def mostrar_validacion():
    eventos_dropdown = list(coleccion_eventos.find({}, {"codigo": 1, "nombre": 1, "_id": 0}))


    rut_ingresado = request.args.get('rut')
    codigo_evento = request.args.get('evento')

    resultado_validacion = None
    estado_actual = None
    nombre_invitado = None

    if rut_ingresado and codigo_evento:
        
        evento_db = coleccion_eventos.find_one({
            "codigo": codigo_evento,
            "invitados.rut": rut_ingresado
        })

        if evento_db:
            for inv in evento_db.get("invitados", []):
                if inv["rut"] == rut_ingresado:
                    estado_actual = inv["estado"]
                    break

            persona = coleccion_invitados.find_one({"rut": rut_ingresado})
            nombre_invitado = persona["nombre"] if persona else rut_ingresado
            
            # 4. Lógica de validación según el estado
            if estado_actual == "confirmado":
                resultado_validacion = "permitido"
            else:
                # Puede estar 'pendiente', 'rechazado', etc.
                resultado_validacion = "bloqueado"
        else:
            # Si el RUT no está en el arreglo de invitados de ese evento
            resultado_validacion = "no_existe"

    return render_template('validacion.html', 
                           eventos_dropdown=eventos_dropdown, 
                           resultado=resultado_validacion, 
                           rut=rut_ingresado,
                           nombre=nombre_invitado,
                           estado=estado_actual)

# 4. Ruta Top 3
@app.route('/top.html')
def mostrar_top():

    pipeline = [

        {"$unwind": "$invitados"},
        

        {"$match": {"invitados.estado": "confirmado"}},
        

        {"$lookup": {
            "from": "invitados",             # Colección con la que queremos cruzar
            "localField": "invitados.rut",   # El campo RUT en nuestro arreglo actual
            "foreignField": "rut",           # El campo RUT en la colección 'invitados'
            "as": "datos_completos"          # Nombre del nuevo arreglo donde guardará el cruce
        }},
        

        {"$group": {
            "_id": "$codigo", 
            "nombre_evento": {"$first": "$nombre"}, # Mantenemos el nombre del evento
            "lugar": {"$first": "$lugar"},          # Mantenemos el lugar
            "total_confirmados": {"$sum": 1}        # Sumamos 1 por cada invitado confirmado que pasó el filtro
        }},
        

        {"$sort": {"total_confirmados": -1}},
        

        {"$limit": 3}
    ]


    top_eventos_db = list(coleccion_eventos.aggregate(pipeline))
    
    return render_template('top.html', top_eventos=top_eventos_db)

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)