from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from models import User, load_user, register_user, get_user_by_username

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'proyecto_gc'
app.config['MYSQL_PASSWORD'] = 'TU_PASSWORD'
app.config['MYSQL_DB'] = 'proyecto_gc'
mysql = MySQL(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader_callback(user_id):
    return load_user(user_id, mysql)

# Rutas
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))

@app.route('/prediccion', methods=['GET', 'POST'])
@login_required
def prediccion():
    resultado = None
    if request.method == 'POST':
        if 'imagen' not in request.files:
            flash('No se seleccionó ninguna imagen', 'danger')
        else:
            imagen = request.files['imagen']
            if imagen.filename == '':
                flash('No se seleccionó ninguna imagen', 'danger')
            else:
                # Guardar temporalmente la imagen
                ruta_temporal = f"static/uploads/{imagen.filename}"
                imagen.save(ruta_temporal)
                
                # Aquí llamamos a la función del ML_Model para predecir
                resultado = predecir_guayaba(ruta_temporal)  # función que definimos en ML_model.py

    return render_template('prediccion.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)
