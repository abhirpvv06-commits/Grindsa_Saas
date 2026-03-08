import os

class Config:
    SECRET_KEY = "super-secret-key-change-this"
    SQLALCHEMY_DATABASE_URI = "sqlite:///grindsa.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "jwt-secret-change-this"