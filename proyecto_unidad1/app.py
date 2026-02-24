from flask import Flask
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from models.user import User, Post

    with app.app_context():
        db.create_all()

    from routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)