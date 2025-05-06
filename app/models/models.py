'''
from ..extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    baja = db.Column(db.Boolean, nullable=False)

    # Relaciones
    ventas = db.relationship('Ventas', backref='usuario', lazy=True)


class Productos(db.Model):
    __tablename__ = 'productos'

    producto_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    baja = db.Column(db.Boolean, nullable=False)

    # Relaciones
    detalle_ventas = db.relationship('DetalleVenta', backref='producto', lazy=True)


class Ventas(db.Model):
    __tablename__ = 'ventas'

    venta_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cantidad_art = db.Column(db.Integer, nullable=False)

    # Relaciones
    detalle_ventas = db.relationship('DetalleVenta', backref='venta', lazy=True)


class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'

    detalle_venta_id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.venta_id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.producto_id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

'''