from ..extensions import db

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
