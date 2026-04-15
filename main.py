from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from strings_configuracio import StringsConfiguracio
from models import db
from models.usuari import Usuari

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

# Crear las tablas si no existen
with app.app_context():
    db.create_all()


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
    inventory_items = [
        {"selected": True, "product": "[E-COM09] Large Desk", "location": "WH/Stock", "on_hand": "1.00", "forecast": "-4.00", "route": "Order Once", "min": "0.00", "max": "0.00", "to_order": "4.00"},
        {"selected": True, "product": "[FURN_9001] Flipover", "location": "WH/Stock", "on_hand": "5.00", "forecast": "-6.00", "route": "Order Once", "min": "0.00", "max": "0.00", "to_order": "6.00"},
        {"selected": False, "product": "[FURN_9666] Table", "location": "WH/Stock", "on_hand": "2.00", "forecast": "-1.00", "route": "Order Once", "min": "0.00", "max": "0.00", "to_order": "1.00"},
        {"selected": False, "product": "[FURN_7777] Office Chair", "location": "WH/Stock/Assemb...", "on_hand": "4.00", "forecast": "4.00", "route": "Buy", "min": "5.00", "max": "10.00", "to_order": "6.00"},
        {"selected": True, "product": "[FURN_8888] Office Lamp", "location": "WH/Stock/Assemb...", "on_hand": "8.00", "forecast": "0.00", "route": "Order Once", "min": "10.00", "max": "10.00", "to_order": "2.00"}
    ]
    return render_template('aplicacion.html', inventory_items=inventory_items)


if __name__ == '__main__':
    app.run(debug=True)
