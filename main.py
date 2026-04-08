#Para activar el venv necesitamos utilizar el comando: .\venv\Scripts\activate

#Hacemos pip freeze > requirements.txt para crear el requirements y updatearlo

from flask import Flask, render_template, request, redirect, url_for, flash
from strings_configuracio import StringsConfiguracio

app = Flask(__name__, template_folder='templates')
app.config.from_object(StringsConfiguracio)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    # Aquí iría la lógica de autenticación
    # Por ahora, redirigir a una página de éxito o algo
    flash('Login exitoso', 'success')
    return redirect(url_for('home'))

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    # Aquí iría la lógica de registro
    # Por ahora, redirigir al login
    flash('Registro exitoso', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

