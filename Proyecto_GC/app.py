from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin

app = Flask(__name__)
app.secret_key = 'cosa1234'

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'proyecto_gc'
app.config['MYSQL_PASSWORD'] = 'cosita1225*'
app.config['MYSQL_DB'] = 'proyecto_gc'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------ User Loader ------------------
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        u = UserMixin()
        u.id = str(user[0])
        u.username = user[1]
        u.password = user[2]
        return u
    return None

# ------------------ Registro ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if not username or not password:
            flash("Usuario y contraseña son obligatorios", "danger")
            return render_template('register.html')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            mysql.connection.commit()
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error al registrar usuario: {str(e)}", "danger")
        finally:
            cur.close()
    return render_template('register.html')

# ------------------ Login ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
        except Exception as e:
            flash(f"Error de base de datos: {str(e)}", "danger")
            return render_template('login.html')
        finally:
            cur.close()

        if user and bcrypt.check_password_hash(user[2], password):
            u = UserMixin()
            u.id = str(user[0])
            u.username = user[1]
            u.password = user[2]
            login_user(u)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrecta", "danger")
    return render_template('login.html')

# ------------------ Dashboard ------------------
@app.route('/dashboard')
@login_required
def dashboard():
    user = {'username': session.get('user_username', 'Usuario')}
    return render_template('dashboard.html', user=user)

# ------------------ Logout ------------------
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('login'))

# ------------------ Ejecutar app ------------------
if __name__ == '__main__':
    app.run(debug=True)
