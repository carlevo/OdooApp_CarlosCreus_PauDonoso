#Para activar el venv necesitamos utilizar el comando: .\venv\Scripts\activate

#Hacemos pip freeze > requirements.txt para crear el requirements y updatearlo

from flask import Flask, render_template, request, redirect, url_for, flash
from strings_configuracio import StringsConfiguracio

app = Flask(__name__, template_folder='templates')
app.config.from_object(StringsConfiguracio)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Aquí iría la lógica de autenticación
        flash('Login exitoso', 'success')
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        # Aquí iría la lógica de registro
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True)

