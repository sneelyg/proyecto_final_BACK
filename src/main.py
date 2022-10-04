"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Marca, Producto
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route ('/login', methods = ['POST'])
def login():
    body = request.get_json()  #Esto hace que e lbody que envia la api sea leido como json.
    one = User.query.filter_by(email=body['email'], password = body['password']).first() #Esto compara el "email" y "password" que llegó desde el body con los de la tabla User.
    if (one is None): 
        raise APIException("Ususario no existe o clave incorrecta", status_code=401)
    else :
        expiracion = datetime.timedelta(minutes=60)
        acceso = create_access_token(identity= body['email'], expires_delta = expiracion)  
        return {
            "login" : "ok",
            "token" : acceso,
            "tiempo" : expiracion.total_seconds()
        }  

@app.route ('/registro', methods = ['POST'])
def registro():
    body = request.get_json()
    #Primero veo que usuario no exista
    existe_mail = User.query.filter_by(email = body['email']).first()
    if (existe_mail is  not None):
        return "El correo utilizado ya existe en la base de datos"
    
    existe_username = User.query.filter_by(username = body['username']).first()
    if (existe_username is  not None):
        return "El nombre de usuario utilizado ya existe en la base de datos"

    else :
            
        new_user = User()
        new_user.email = body['email']
        new_user.password = body['password']
        new_user.is_active = True
        new_user.username = body['username']
        new_user.nombre = body['nombre']
        new_user.apellido = body['apellido']
        new_user.rut = body['rut']

        db.session.add(new_user)
        db.session.commit()
        return "Usuario Nuevo Creado" 
###
{
"email": "santiagoneely@123.cl",
    "password" : "123456",
    "is_active" : "True",
    "username":"Sneely",
    "nombre":"Santi",
    "apellido":"neely",
    "rut":"12345"
}

###
@app.route ('/marcas/registro', methods = ['POST'])
def marcas_registro():
    body = request.get_json()
    #Primero veo que usuario no exista
    existe_marca = Marca.query.filter_by(nombre_marca = body['nombre_marca']).first()
    if (existe_marca is  not None):
        return "El nombre de marca ya existe"

    else:
        new_marca = Marca()
        new_marca.vendedor = body ['vendedor']
        new_marca.nombre_marca = body ['nombre_marca']
        new_marca.direccion = body ['direccion']
        new_marca.descripcion = body ['descripcion']
        new_marca.tipo_pago = body ['tipo_pago']
        new_marca.banco_cuenta = body ['banco_cuenta']
        new_marca.tipo_cuenta = body ['tipo_cuenta']
        new_marca.numero_cuenta = body ['numero_cuenta']
        new_marca.rut_cuenta = body ['rut_cuenta']

        db.session.add(new_marca)
        db.session.commit()
        return "Nueva Marca Creada " 

@app.route ('/productos/registro', methods = ['POST'])
def productos_registro():
    nuevo_producto = Producto()
    nuevo_producto.vendedor = body['vendedor']
    nuevo_producto.marca = body['marca']
    nuevo_producto.nombre_producto = body['nombre_producto']
    nuevo_producto.descripcion = body['descripcion']
    nuevo_producto.precio = body['precio']
    nuevo_producto.url_foto = body['url_foto']

    return "Producto Registrado"

@app.route ('/recuperar_clave', methods = ['POST'])
def recuperar_clave():    
    return "Recuperar Clave"


@app.route('/marcas/<int:id_marca>', methods=['GET'])
def una_marca(id_marca):
    una_marca = Marca.query.get(id_marca)
    return jsonify(una_marca.serialize())

@app.route('/productos/<int:id_producto>', methods=['GET'])
def un_producto(id_producto):
    un_producto = Producto.query.get(id_producto)
    return jsonify(un_producto.serialize())

@app.route('/marcas', methods=['GET'])
def todas_las_marcas():
    marcas = Marca.query.all()
    marcas = list(map (lambda marca : marca.serialize(),  marcas))
    return jsonify( marcas)

@app.route('/productos', methods=['GET'])
def todos_los__productos():
    productos = Producto.query.all()
    productos = list(map (lambda productos : productos.serialize(),  productos))
    return jsonify( productos)


@app.route('/productos/<int:id_producto>', methods=['DELETE'])
def borrar_un_producto(id_producto):
    one = Producto.query.filter_by(id = id_producto).first() #first hace que sea el primer elemento , sino, el método filter_by entrega un Arreglo de resultados
    if (one): 
        db.session.delete(one)
        db.session.commit()
        return "Producto Eliminado"
    else :
        raise APIException("Personaje no existe en favoritos", status_code=404 )









# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
