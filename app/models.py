from .extensions import db

class Usuario(db.Model):
    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    baja = db.Column(db.Boolean, nullable=False)


class Productos(db.Model):
    producto_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    baja = db.Column(db.Boolean, nullable=False)

class Ventas(db.Model):
    venta_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cantidad_art = db.Clumn(db.Integer, nullable=False)

class DetalleVenta(db.Model):
    detalle_venta_id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.venta_id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.producto_id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)


usuario_vendedor = db.relationship('Usuario', 'Ventas', backref='usuario_vendedor', lazy=True)
producto_vendedor = db.relationship('Productos', 'DetalleVenta', backref='producto_vendedor', lazy=True)
venta_producto = db.relationship('Ventas', 'DetalleVenta', backref='detalle_ventas', lazy=True)