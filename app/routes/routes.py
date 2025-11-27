from flask import Blueprint, request, jsonify
from app.models import Client
from app import db
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/test")
def test():
    return jsonify({"message": "Routes working!"})

@routes_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if Client.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Client already exists"}), 400

    client = Client(email=data['email'], role=data['role'], surname=data['surname'], given_name=data['given_name'], phone_number=data['phone_number'], location=data['location'], hair_type=data['hair_type'], password=data['password'])
    client.set_password(data['password'])
    db.session.add(client)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

from flask_jwt_extended import create_access_token

@routes_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    client = Client.query.filter_by(email=data['email']).first()
    
    if client and client.check_password(data['password']):
        access_token = create_access_token(
            identity=str(client.id),
            additional_claims={
                "role": client.role,
                "email": client.email
            }
        )
        return {"access_token": access_token}, 200
    
    return {"msg": "Invalid credentials"}, 401


@routes_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    client = Client.query.get(user_id)
    return jsonify({"message": f"Hello, {client.email}!"}), 200