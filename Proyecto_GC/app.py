from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, load_user, register_user, get_user_by_username
from predict_guayaba import predict_guayaba  # Importa tu función de predicción

import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "tu_clave_secreta"

# Configuración MySQL
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('proyecto_gc')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('proyecto_gc')

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader_callback(user_id):
    return load_user(user_id, mysql)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username, mysql)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrecta", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user, error = register_user(username, password, mysql)
        if user:
            flash("Registro exitoso. Por favor inicia sesión.", "success")
            return redirect(url_for('login'))
        else:
            flash(f"Error al registrar usuario: {error}", "danger")
    return render_template('registro.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/quienessomos')
@login_required
def quienes_somos():
    return render_template('MisionVision.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))


@app.route('/prediccion', methods=['GET', 'POST'])
@login_required
def prediccion():
    label = None
    confidence = None
    image_path = None

    if request.method == 'POST':
        imagen = request.files.get('file')
        if not imagen or imagen.filename == '':
            flash('No se seleccionó ninguna imagen', 'danger')
        else:
            ruta_temporal = os.path.join(UPLOAD_FOLDER, imagen.filename)
            imagen.save(ruta_temporal)

            label, confidence = predict_guayaba(ruta_temporal)
            image_path = url_for('static', filename=f'uploads/{imagen.filename}')

    return render_template(
        'prediccion.html',
        label=label,
        confidence=confidence,
        image_path=image_path
    )


if __name__ == '__main__':
    app.run(debug=True)
