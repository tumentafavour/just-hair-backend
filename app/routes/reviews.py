from flask import Blueprint, request, jsonify
from app.models import Review
from app import db,limiter
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token
from datetime import timedelta
    # db.init_app(app)
    # migrate.init_app(app, db)    # db.init_app(app)
    # migrate.init_app(app, db)

reviews_bp = Blueprint("reviews", __name__)




#/ start of endpoint to retrieve or add a new review
@reviews_bp.route('/api/reviews', methods=['POST'])
def add_reviews():
    data = request.get_json()
    new_reviews = Review(title = data['title'], description = data['description'], serviceProvider=data['serviceProvider'], client=data['client'], rating=data['rating'])

    db.session.add(new_reviews)
    db.session.commit()
    return jsonify(new_reviews.to_dict()), 201

#/start of endpoint to get all reviews
@reviews_bp.route('/api/reviews', methods=['GET'])
def get_reviews():
    all_reviews= Review.query.all()
    return jsonify([Review.to_dict() for reviews in all_reviews]), 200


#/start of endpoint to update all reviews
    
@reviews_bp.route('/api/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    data = request.get_json()
    review = Review.query.get(id)
    if not review:
        return jsonify({"error": "review not found"}), 404
    review.title = data.get('title', review.title)
    review.description = data.get('description', review.description)
    review.serviceProvider =data.get('serviceProvider', review.serviceProvider)
    review.client=data.get('client', review.client)
    review.rating=data.get('rating',review.rating)
    db.session.commit()
    return jsonify(review.to_dict()), 200




#/start point of delete a note

@reviews_bp.route('/api/review/<int:id>', methods=['DELETE'])
def delete_reviews(id):
    review = Review.query.get(id)
    if not review:
        return jsonify({"error": "review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "review deleted successfully"})

    