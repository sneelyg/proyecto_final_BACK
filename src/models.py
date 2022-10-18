from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(120), unique=False, nullable=False)
    apellido = db.Column(db.String(120), unique=False, nullable=False)
    rut = db.Column(db.Integer, unique=True, nullable=False)
    nombre_marca = db.Column(db.String(80), unique=True, nullable=False)
    direccion = db.Column(db.String(250), unique=False, nullable=False)
    descripcion = db.Column(db.String(250), unique=False, nullable=False)
    tipo_pago = db.Column(db.String(250), unique=False, nullable=False)
    banco_cuenta = db.Column(db.String(250), unique=False, nullable=True)
    tipo_cuenta = db.Column(db.String(50), unique=False, nullable=True)
    numero_cuenta = db.Column(db.Integer, unique=True, nullable=True)
    



    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "usuario" : self.username,
            "nombre" : self.nombre,
            "apellido":self.apellido,
            "marca": self.nombre_marca,
            "descricpion":self.descripcion,
            "direccion":self.direccion,
            "tipo_pago":self.tipo_pago,
            "banco":self.banco_cuenta,
            "tipo_cuenta":self.tipo_cuenta,
            "numero_cuenta":self.numero_cuenta,
            "rut_cuenta":self.rut_cuenta

            # do not serialize the password, its a security breach
        }


class Producto (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendedor = db.Column(db.Integer, db.ForeignKey('user.id'))
    nombre_producto = db.Column(db.String(250), unique=False, nullable=False)
    descripcion = db.Column(db.String(250), unique=False, nullable=False)
    precio =  db.Column(db.Integer, unique=True, nullable=False)
    url_foto = db.Column(db.String(250), unique=True, nullable=True)
    
    rel_user = db.relationship('User')
   

    def __repr__(self):
        return '<Producto %r>' % self.nombre_producto
    
    def serialize(self):
        return {
            "id": self.id,
            "vendedor":self.vendedor,
            "producto": self.nombre_producto,
            "descricpion":self.descripcion,
            "precio": self.precio,
            "url_foto": self.url_foto
        }
