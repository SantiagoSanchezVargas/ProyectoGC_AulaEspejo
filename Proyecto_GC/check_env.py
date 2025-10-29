"""
Script rápido para comprobar si las librerías necesarias están instaladas.
Ejecutar: python Proyecto_GC/check_env.py

Imprime qué paquetes faltan y sugiere comandos pip para instalarlos en Windows (PowerShell).
"""

modules = {
    'flask': 'Flask',
    'flask_mysqldb': 'Flask-MySQLdb (requires mysqlclient on Windows)',
    'flask_login': 'Flask-Login',
    'flask_bcrypt': 'Flask-Bcrypt',
    'mysql': 'mysql-connector-python',
    'tensorflow': 'tensorflow (or tensorflow-cpu if no GPU)',
    'PIL': 'pillow',
    'numpy': 'numpy',
    'sklearn': 'scikit-learn',
    'cv2': 'opencv-python'
}

missing = []
for mod, pkg in modules.items():
    try:
        __import__(mod)
    except Exception:
        missing.append((mod, pkg))

if not missing:
    print("Parece que todas las librerías principales están instaladas.")
else:
    print("Faltan las siguientes librerías (módulo -> paquete pip recomendado):")
    for mod, pkg in missing:
        print(f" - {mod} -> {pkg}")

    print('\nSugerencia de instalación (PowerShell):')
    pkgs = ' '.join(set(pkg.split(' ')[0] for _, pkg in missing))
    print(f"pip install {pkgs}")

    print('\nNotas:')
    print(' - En Windows, "Flask-MySQLdb" suele necesitar "mysqlclient" y compiladores; si tienes problemas, considera usar "mysql-connector-python" o cambiar la extensión a Flask-MySQL-Connector.')
    print(' - Para TensorFlow en CPU, prueba "tensorflow-cpu" si no tienes GPU o fallan las instalaciones.')
