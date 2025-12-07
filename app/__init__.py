
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
import os
from flask_swagger_ui import get_swaggerui_blueprint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint
import os



limiter = Limiter(key_func=get_remote_address, default_limits=["500 per day", "100 per hour"])  # no app yet


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)


    # swagger
    from flask_swagger_ui import get_swaggerui_blueprint

    
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,API_URL,config={'app_name':"API"}
    )
    app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)

    # Initialize extensions
    # db.init_app(app)
    # migrate.init_app(app, db)

    @app.route("/")
    def index():
        return "Welcome to Just Hair Backend!"

    # Import models so migrations can detect them
    from app import models

    # Register routes (Blueprints)
    from app.routes.routes import routes_bp
    app.register_blueprint(routes_bp)
   
        
    from app.routes.reviews import  reviews_bp
    app.register_blueprint(reviews_bp)
    
 
    from app.routes.client import client_bp
    app.register_blueprint(client_bp)
  
    from app.routes.hairattachment import hairattachment_bp
    app.register_blueprint(hairattachment_bp)
    from app.routes.serviceprovider import serviceprovider_bp
    app.register_blueprint(serviceprovider_bp)

    return app



# app = create_app()
