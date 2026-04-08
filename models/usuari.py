from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db


class Usuari(UserMixin, db.Model):
    __tablename__ = 'usuaris'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuari {self.email}>'
