from models import db


class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False, default='WH/Stock')
    en_stock = db.Column(db.Float, nullable=False, default=0.0)
    prevision = db.Column(db.Float, nullable=False, default=0.0)
    a_pedir = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f'<Producto {self.nombre}>'
