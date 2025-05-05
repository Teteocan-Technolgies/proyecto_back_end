from flask import Blueprint, jsonify
from .models import Usuario

api = Blueprint('api', __name__)

@api.route('/')
def list_users():
    return jsonify(Usuario.query.all())
