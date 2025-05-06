from ..extensions import db

class Ventas(db.Model):
    __tablename__ = 'ventas'

    venta_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cantidad_art = db.Column(db.Integer, nullable=False)

    # Relaciones
    detalle_ventas = db.relationship('DetalleVenta', backref='venta', lazy=True)
