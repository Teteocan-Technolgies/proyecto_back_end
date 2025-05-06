from app.models import Usuario
from flask import Blueprint, jsonify
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


def get_data_usuario(data):
    data_usuario = Usuario.query.filter_by(Usuario.usuario_id == data['usuario_id']).first()
    return {
        "nombre": data_usuario.nombre,
        "apellido": data_usuario.apellido,
        "email": data_usuario.email,
        "usuario_id": data_usuario.usuario_id,
    }


def registrar_usuario(data):
    #Verificar si el usuario ya existe en la base de datos
    usuario_existente = Usuario.query.filter_by(email=data['email']).first()
    if usuario_existente:
        return {
            "mensaje": "El usuario ya existe"
        }, 400
    

    #Crear un nuevo usuario
    hashed_password = generate_password_hash(data['password'], method='sha256')

    nuevo_usuario = Usuario(
        nombre = data['nombre'],
        apellido = data['apellido'],
        email = data['email'],
        password = hashed_password,
        baja = False,
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return {
        "mensaje": "Usuario registrado con éxito",
        "usuario":nuevo_usuario
    }

def login_usuario(data):
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if usuario and check_password_hash(usuario.password, data['password']):
        return {
            "mensaje": "Inicio de sesión exitoso",
            "usuario_id": usuario.usuario_id,
            "nombre": usuario.nombre,
            "apellido" : usuario.apellido
        }
    else:
        return {
            "mensaje": "Credenciales incorrectas"
        }, 401