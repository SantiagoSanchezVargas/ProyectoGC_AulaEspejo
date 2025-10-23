from flask_login import UserMixin

# ------------------ Clase User ------------------
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = str(id)  # Flask-Login espera string
        self.username = username
        self.password = password

# ------------------ Funciones auxiliares ------------------
def get_user_by_id(db_connection, user_id):
    cur = db_connection.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

def get_user_by_username(db_connection, username):
    cur = db_connection.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None
