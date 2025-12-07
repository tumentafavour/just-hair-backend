from flask import Blueprint, request, jsonify
from app.models import ServiceProvider
from app import db
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token

serviceprovider_bp = Blueprint('serviceprovider_bp', __name__)

#this route is to get all service providers
@serviceprovider_bp.route ('/api/serviceproviders', methods=['GET'])
def get_serviceproviders():
    all_serviceproviders = ServiceProvider.query.all()
    return jsonify([serviceprovider.to_dict() for serviceprovider in all_serviceproviders])

#this route creates a new service provider
@serviceprovider_bp.route ('/api/serviceproviders' , methods=['POST'])
def add_serviceprovider():
    try:
        data = request.get_json()
        new_serviceprovider = ServiceProvider(role=data['role'], surname=data['surname'], given_name=data['given_name'], id_card_number=data['id_card_number'], phone_number=data['phone_number'], location=data['location'], about=data['about'], email=data['email'], password=data['password'])
        db.session.add(new_serviceprovider)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "error", "error": f"{e}"}), 400
    return jsonify(new_serviceprovider.to_dict()), 201