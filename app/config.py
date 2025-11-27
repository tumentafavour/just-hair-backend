import os

class Config:
    
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:yan@localhost:5432/just_hair_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-key"  # change in production
