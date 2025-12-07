from flask import Blueprint, request, jsonify
from app.models import Client
from app import db,limiter
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from datetime import timedelta
    

client_bp = Blueprint("client", __name__)




#/ start of endpoint to retrieve or add a new client
@client_bp.route('/api/client', methods=['POST'])
def add_client():
    data = request.get_json()
    new_client =Client(surname=data['surname'],given_name=data['given_name'],email=data['email'],role=data['role'],picture=data['picture'],phone_number=data['phone_number'],location=data['location'],hair_type=data['hairtype'],password=data['password'])

    db.session.add(new_client)
    db.session.commit()
    return jsonify(new_client.to_dict()), 201


#/start of endpoint to get all client
@client_bp.route('/api/client', methods=['GET'])
def fetch_client():
    all_client=Client.query.all()
    return jsonify([client.to_dict() for client in all_client]), 200


#/start of  new endpoint to get client based on id
@client_bp.route('/api/client/<int:id>', methods=['GET'])
def get_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "client not found"}), 404
    return jsonify(client.to_dict()), 200
#/end of endpoint





    
#/start point of delete all client
@client_bp.route('/api/client', methods=['DELETE'])
def delete_client():
    db.session.query(Client).delete()
    db.session.commit()
    return jsonify({"message": "clientdeleted successfully"})
#/endpoint of delete all client


#/start point to delete a client

@client_bp.route('/api/client/<int:id>', methods=['DELETE'])
def remove_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "client not found"}), 404
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "client deleted successfully"})

