from ..extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    baja = db.Column(db.Boolean, nullable=False)

    # Relaciones
    ventas = db.relationship('Ventas', backref='usuario', lazy=True)