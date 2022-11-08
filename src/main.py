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
from models import db, User, Producto
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import messagebird
import random
import string
import math


# from models import Person

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

@app.route('/privada')
@jwt_required()
def privada():
    mail_usuario = get_jwt_identity()
    usuario = User.query.filter_by(email = mail_usuario).first()
    if not (usuario is None):
        print (usuario)
        print("hola")
    else:
        print ("usuario no encontrado")
    return jsonify({"success": "ok", "usuario": mail_usuario}), 200




@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/login', methods=['POST'])
def login():
    # Esto hace que e lbody que envia la api sea leido como json.
    body = request.get_json()
    # Esto compara el "email" y "password" que llegó desde el body con los de la tabla User.
    one = User.query.filter_by(
        email=body['email'], password=body['password']).first()
    if (one is None):
        raise APIException(
            "Ususario no existe o clave incorrecta", status_code=401)
    else:
        expiracion = datetime.timedelta(minutes=600)
        acceso = create_access_token(
            identity=body['email'], expires_delta=expiracion)
        return {
            "login": "ok",
            "token": acceso,
            "tiempo": expiracion.total_seconds()
        }
"""Para Login
    {
"email": "santiagoneely@123.cl",
    "password" : "12345"}
        # 
"""

@app.route ('/registro', methods = ['POST'])

def registro():
    body = request.get_json()
    # Primero veo que usuario no exista
    print (body)
    existe_mail = User.query.filter_by(email = body['email']).first()
    if (existe_mail is  not None):
        return {
            "registro": "not",
            "message" : "El correo utilizado ya existe"
        }
    
    existe_username = User.query.filter_by(username = body['username']).first()
    if (existe_username is  not None):
        return {
            "registro": "not",
            "message" : "Nombre de Usuario  ya existe. Usuario no creado"
        }

    existe_rut = User.query.filter_by(rut = body['rut']).first()
    if (existe_rut is  not None):
        return {
            "registro": "not",
            "message" : "RUT ya existen, usuario no creado"
        }
    else :     
        new_user = User()
        new_user.email = body['email']
        new_user.password = body['password']
        new_user.is_active = True
        new_user.username = body['username']
        new_user.nombre = body['nombre']
        new_user.apellido = body['apellido']
        new_user.rut = body['rut']
        new_user.nombre_marca = body ['nombre_marca']
        new_user.direccion = body ['direccion']
        new_user.descripcion = body ['descripcion']
        new_user.tipo_pago = body ['tipo_pago']
        new_user.banco_cuenta = body ['banco_cuenta']
        new_user.tipo_cuenta = body ['tipo_cuenta']
        new_user.numero_cuenta = body ['numero_cuenta']
        new_user.telefono = body ['telefono']


        db.session.add(new_user)
        db.session.commit()
        return {
            "registro": "ok"
        }
# Para registrar un usuario
"""{
    "email": "santiagoneely@123.cl",
    "password" : "123456",
    "is_active" : "True",
    "username":"Sneely",
    "nombre":"Santi",
    "apellido":"neely",
    "rut":"12345",
    "nombre_marca" : "Zapallos El Rodallo",
    "descripcion":"Hacemos los mejores productos de Zapallo",
    "direccion" : "siempreviva 123, La Cisterna",
    "tipo_pago":"Transferencia",
    "banco_cuenta":"Estado",
    "tipo_cuenta":"rut",
    "numero_cuenta" : "1234556"
    }

"""

@app.route ('/productos/registro', methods = ['POST'])
@jwt_required()

def productos_registro():
 

    body = request.get_json()
    print (body)

    nuevo_producto = Producto()
    nuevo_producto.vendedor = body['vendedor']
    nuevo_producto.marca = body['marca']
    nuevo_producto.nombre_producto = body['nombre_producto']
    nuevo_producto.descripcion = body['descripcion']
    nuevo_producto.precio = body['precio']
    nuevo_producto.url_foto = body['url_foto']

    db.session.add(nuevo_producto)
    db.session.commit()
    return "Producto Registrado"


"""
{
"vendedor": "1",
    "marca" : "1",
    "nombre_producto" : "Pure de Zapallo",
    "descripcion":"Piure de Zapallo dulce, 600 gr",
    "precio":"10000",
    "url_foto":"url_de_prueba"
}

"""

@app.route ('/recuperar/clave', methods = ['POST'])
def recuperar_clave():    
    body = request.get_json()  #Esto hace que e lbody que envia la api sea leido como json.
    existe_usuario = User.query.filter_by(email=body['email']).first() #Esto compara el "email"  que llegó desde el body con los de la tabla User.
    telefono = body['telefono']
    if (existe_usuario is None): 
        raise APIException("Ususario no existe en la base de datos", status_code=401)
    else :
        expiracion = datetime.timedelta(minutes=100)
        acceso = create_access_token(identity= body['email'], expires_delta = expiracion)  
        x = random.random()
        y=x*100000000
        z=math.trunc(y)
        existe_usuario.password=z
        db.session.commit() 
        print("Clave cambiada")
        sms(telefono, z )


        

        return {
            "email" : body['email'],
            "nueva clave" : z,
        }  


@app.route ('/cambiar/clave', methods = ['POST'])
@jwt_required()
def cambiar_clave():    
    print("Cambiando Clave")
    body = request.get_json()  #Esto hace que e lbody que envia la api sea leido como json.
    mail_usuario = get_jwt_identity()
    usuario = User.query.filter_by(password = body['old_password'] , email=mail_usuario).first() #Esto compara el "email"  que llegó desde el body con los de la tabla User.
   
    if (usuario is None): 
        raise APIException("Ususario no existe en la base de datos, o clave incorrecta", status_code=401)
    else :
        usuario.password = body['new_password']
        db.session.commit()
    
        return {
            "succes" : "ok",
        } 




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
        raise APIException("Producto no Existe, o ya ha sido eliminado", status_code=404 )

###pA3SuFath8wM4iRHE750SCPSc  //Llave maca
###

def sms(number, clave):
    print("enviando mensaje")
    mensaje = "Tu nueva contraseña es " + str(clave)
    client = messagebird.Client("jYVEJbNy2HrchxysmH6xSgN26")
    message = client.message_create(
              'TestMessage',
              number,
              mensaje,
              { 'reference' : 'Foobar' }
          )



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
