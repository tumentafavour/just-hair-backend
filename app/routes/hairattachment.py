from flask import Blueprint, request, jsonify
from app.models import HairAttachment
from app import db
from flask_migrate import Migrate
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token




hairattachment_bp = Blueprint('hairattachment_bp', __name__)



#this route is to get all hairattachments
@hairattachment_bp.route ('/api/hairattachments', methods=['GET'])
def get_hairattachments():
    all_hairattachments = HairAttachment.query.all()
    return jsonify([hairattachment.to_dict() for hairattachment in all_hairattachments])

#this route creates a new a hair attachments
@hairattachment_bp.route ('/api/hairattachments' , methods=['POST'])
def add_hairattachment():
    try:
        data = request.get_json()
        new_hairattachment = HairAttachment(picture=data['picture'], name=data['name'], color=data['color'], texture=data['texture'], length=data['length'], brand=data['brand'], price=data['price'], type=data['type'], description=data['description'])
        db.session.add(new_hairattachment)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "error", "error": f"{e}","trace": "check data types and required fields"}), 400
    return jsonify(new_hairattachment.to_dict()), 201


#this route updates all hair attachments
@hairattachment_bp.route('/api/hairattachment/<int:id>', methods=['PUT'])
def update_hairattachment(id):
    data = request.get_json()
    hairattachment = HairAttachment.query.get(id)
    if not hairattachment:
        return jsonify({"error": "hairattachment not found"}), 404
    hairattachment.picture = data.get('picture', hairattachment.picture)
    hairattachment.name = data.get('name', hairattachment.name)
    hairattachment.color =data.get('color', hairattachment.color)
    hairattachment.length = data.get('length', hairattachment.length)
    hairattachment.texture = data.get('texture', hairattachment.texture)
    hairattachment.brand = data.get('brand', hairattachment.brand)
    hairattachment.price = data.get('price', hairattachment.price)
    hairattachment.type = data.get('type', hairattachment.type)
    hairattachment.description = data.get('description', hairattachment.description)
    db.session.commit()
    return jsonify(hairattachment.to_dict()), 200



#this sixth route deletes a note based on id
@hairattachment_bp.route('/api/hairattachment/<int:id>', methods=['DELETE'])
def delete_hairattachment(id):
    hairattachment = HairAttachment.query.get(id)
    if not hairattachment:
        return jsonify({"error": "hair attachment not found"}), 404
    db.session.delete(hairattachment)
    db.session.commit()
    return jsonify({"message": "hair attachment deleted successfully"})




