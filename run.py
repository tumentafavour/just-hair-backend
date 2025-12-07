from app import create_app
from app import db



app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


from flask import Flask, request, jsonify
from app import db






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
