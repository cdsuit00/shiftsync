from flask import Flask, jsonify
from config import Config
from extensions import db, migrate, jwt
from routes.auth import bp as auth_bp
from routes.shifts import bp as shifts_bp
from routes.timeoff import bp as timeoff_bp
from routes.users import bp as users_bp
from routes.schedules import bp as schedules_bp
from models import User, Shift, TimeOffRequest

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(shifts_bp)
    app.register_blueprint(timeoff_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(schedules_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
