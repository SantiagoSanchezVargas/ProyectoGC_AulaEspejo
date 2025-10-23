from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Función para cargar usuario por id
def load_user(user_id, mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

# Función para registrar un usuario
def register_user(username, password, mysql):
    password_hash = generate_password_hash(password)
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password_hash))
        mysql.connection.commit()
        user_id = cur.lastrowid
    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return None, str(e)
    cur.close()
    return User(user_id, username, password_hash), None

# Función para buscar usuario por username (login)
def get_user_by_username(username, mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2])
    return None
