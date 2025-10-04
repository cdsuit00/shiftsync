# Run: FLASK_APP=app.py flask shell
# then: >>> from create_manager import create_manager; create_manager('admin','admin@example.com','password')
from app import create_app
from extensions import db
from models import User

def create_manager(username, email, password):
    app = create_app()
    with app.app_context():
        if User.query.filter((User.username == username) | (User.email == email)).first():
            print("User exists")
            return
        u = User(username=username, email=email, role="manager")
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        print("Manager created:", username)
