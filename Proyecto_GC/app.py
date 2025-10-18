from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "clave_secreta_para_flash"  # Cambia por algo seguro en producción

DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'proyecto_gc',
    'password': 'cosita1225*',
    'database': 'proyecto_gc'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# =========================
# Decorador para proteger rutas
# =========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Debes iniciar sesión", "danger")
            return redirect(url_for('login_get'))
        return f(*args, **kwargs)
    return decorated_function

# =========================
# Registro
# =========================
@app.route('/registro', methods=['GET'])
def registro_get():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registro_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirmar = request.form.get('confirm_password')

    if not username or not password or not confirmar:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('registro_get'))

    if password != confirmar:
        flash("Las contraseñas no coinciden", "danger")
        return redirect(url_for('registro_get'))

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Verificar si el username ya existe
        cursor.execute("SELECT id FROM users WHERE username=%s LIMIT 1", (username,))
        if cursor.fetchone():
            flash("El usuario ya está registrado", "danger")
            return redirect(url_for('registro_get'))

        # Guardar usuario con contraseña hasheada
        hashed = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()

        flash("Usuario registrado exitosamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login_get'))

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# =========================
# Login
# =========================
@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Faltan usuario o contraseña", "danger")
        return redirect(url_for('login_get'))

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password FROM users WHERE username=%s LIMIT 1", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # Login exitoso → guardar sesión
            session['user_id'] = user['id']
            session['user_username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales inválidas", "danger")
            return redirect(url_for('login_get'))

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# =========================
# Dashboard protegido
# =========================
@app.route('/dashboard')
@login_required
def dashboard():
    user = {'username': session['user_username']}
    return render_template('dashboard.html', user=user)

# =========================
# Logout
# =========================
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('login_get'))

# =========================
# Ruta inicial
# =========================
@app.route('/')
def index():
    return redirect(url_for('login_get'))

# =========================
# Ejecutar App
# =========================
if __name__ == "__main__":
    app.run(debug=True)
