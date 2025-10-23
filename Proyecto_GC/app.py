from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'Cosa1234'

# ------------------ Configuración MySQL ------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'proyecto_gc'
app.config['MYSQL_PASSWORD'] = 'cosita1225*'
app.config['MYSQL_DB'] = 'proyecto_gc'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Login User Class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(str(user[0]), user[1], user[2])
    return None

# ------------------ Rutas ------------------

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

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
            u = User(str(user[0]), user[1], user[2])
            login_user(u)
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrecta", "danger")

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('login'))


@app.route("/test-db")
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return "Conexión exitosa a la base de datos!"
    except Exception as e:
        return f"Error de conexión: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
