from app.models import Usuario
from flask import Blueprint, jsonify
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


def get_all_users() :
    # Obtener todos los usuarios de la base de datos
    usuarios = Usuario.query.all()
    # Convertir los usuarios a un formato JSON
    usuarios_json = [usuario.to_dict() for usuario in usuarios]
    # Devolver la lista de usuarios en formato JSON
    return jsonify(usuarios_json)

def get_data_usuario(data):
    data_usuario = Usuario.query.filter_by(usuario_id=data['usuario_id']).first()
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
    

    print("usuario_existente:", usuario_existente)
    #Crear un nuevo usuario
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)

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
        "usuario": {
            "nombre": nuevo_usuario.nombre,
            "apellido": nuevo_usuario.apellido,
            "email": nuevo_usuario.email,
            "usuario_id": nuevo_usuario.usuario_id
        }
    }, 201

def login_usuario(data):
    print("Entramos")
    usuario = Usuario.query.filter_by(email=data['email']).first()
    print("usuario")
    print(usuario)
    if usuario and check_password_hash(usuario.password, data['password']):
        print("Todo en orden")
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