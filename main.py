from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from strings_configuracio import StringsConfiguracio
from models import db
from models.usuari import Usuari
from models.producto import Producto

app = Flask(__name__, template_folder='templates')
app.config.from_object(StringsConfiguracio)

# Inicializar base de datos
db.init_app(app)

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Has d\'iniciar sessió per accedir a aquesta pàgina.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuari, int(user_id))

# Crear las tablas si no existen y sembrar productos iniciales
with app.app_context():
    db.create_all()
    if Producto.query.count() == 0:
        productos_iniciales = [
            Producto(nombre="[E-COM09] Large Desk", ubicacion="WH/Stock", en_stock=1.0, prevision=-4.0, a_pedir=4.0),
            Producto(nombre="[FURN_9001] Flipover", ubicacion="WH/Stock", en_stock=5.0, prevision=-6.0, a_pedir=6.0),
            Producto(nombre="[FURN_9666] Table", ubicacion="WH/Stock", en_stock=2.0, prevision=-1.0, a_pedir=1.0),
            Producto(nombre="[FURN_7777] Office Chair", ubicacion="WH/Stock/Assemb...", en_stock=4.0, prevision=4.0, a_pedir=6.0),
            Producto(nombre="[FURN_8888] Office Lamp", ubicacion="WH/Stock/Assemb...", en_stock=8.0, prevision=0.0, a_pedir=2.0),
        ]
        db.session.add_all(productos_iniciales)
        db.session.commit()


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homescreen'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Usuari.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Sessió iniciada correctament!', 'success')
            return redirect(url_for('homescreen'))
        else:
            flash('Email o contrasenya incorrectes.', 'danger')

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('homescreen'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            flash('Les contrasenyes no coincideixen.', 'danger')
            return render_template('registro.html')

        if Usuari.query.filter_by(email=email).first():
            flash('Ja existeix un compte amb aquest email.', 'danger')
            return render_template('registro.html')

        user = Usuari(nombre=nombre, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Benvingut/da, {nombre}! Compte creat correctament.', 'success')
        return redirect(url_for('homescreen'))

    return render_template('registro.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessió tancada.', 'info')
    return redirect(url_for('login'))


@app.route('/homescreen')
@login_required
def homescreen():
    return render_template('homeScreen.html')


@app.route('/aplicacion')
@login_required
def aplicacion():
    productos = Producto.query.all()
    return render_template('aplicacion.html', inventory_items=productos)


@app.route('/aplicacion/añadir', methods=['POST'])
@login_required
def añadir_producto():
    nombre = request.form.get('nombre', '').strip()
    ubicacion = request.form.get('ubicacion', 'WH/Stock').strip()
    en_stock = float(request.form.get('en_stock', 0))
    prevision = float(request.form.get('prevision', 0))
    a_pedir = float(request.form.get('a_pedir', 0))

    if not nombre:
        flash('El nombre del producto es obligatorio.', 'danger')
        return redirect(url_for('aplicacion'))

    producto = Producto(nombre=nombre, ubicacion=ubicacion, en_stock=en_stock,
                        prevision=prevision, a_pedir=a_pedir)
    db.session.add(producto)
    db.session.commit()
    flash(f'Producto "{nombre}" añadido correctamente.', 'success')
    return redirect(url_for('aplicacion'))


@app.route('/aplicacion/eliminar/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    producto = db.session.get(Producto, producto_id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
        flash(f'Producto "{producto.nombre}" eliminado.', 'info')
    return redirect(url_for('aplicacion'))


if __name__ == '__main__':
    app.run(debug=True)
