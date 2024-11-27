"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for  # type: ignore
from flask_cors import CORS  # type: ignore
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Crear el objeto de la familia Jackson con miembros iniciales
jackson_family = FamilyStructure("Jackson")
jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

# Manejar errores personalizados como JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtener todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Obtener un miembro específico por ID
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        raise APIException("Member not found", status_code=404)
    return jsonify(member), 200

# Agregar un nuevo miembro a la familia
@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    if not body:
        raise APIException("You must provide the member data", status_code=400)
    if "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
        raise APIException("Missing required fields: first_name, age, lucky_numbers", status_code=400)
    
    new_member = jackson_family.add_member(body)
    return jsonify(new_member), 200

# Eliminar un miembro de la familia por ID
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    success = jackson_family.delete_member(id)
    if not success:
        raise APIException("Member not found", status_code=404)
    return jsonify({"done": True}), 200

# Ejecutar el servidor si se ejecuta directamente el script
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)