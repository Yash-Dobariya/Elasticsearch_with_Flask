from flask import Flask
from src.user.route import user
from src.database import es


def create_app():
    """create app for flask"""
    
    app = Flask(__name__)
    app.register_blueprint(user)
    return app


main_app = create_app()
