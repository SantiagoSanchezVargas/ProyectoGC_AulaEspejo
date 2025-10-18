from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import mysql, bcrypt, login_manager  # <--- Importa desde extensions
from models import User, load_user  # ahora no causa ciclo

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'proyecto_GC'
app.config['MYSQL_PASSWORD'] = 'tu_password'
app.config['MYSQL_DB'] = 'proyecto_gc'

# Inicializar extensiones con app
mysql.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---- Rutas (registro, login, dashboard, logout) ----
@app.route('/')
def home():
    return redirect(url_for('login'))

# (tu código de rutas aquí igual que antes...)

if __name__ == '__main__':
    app.run(debug=True)
