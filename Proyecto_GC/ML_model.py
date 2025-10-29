import cv2
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def cargar_imagenes(carpeta):
    X, y = [], []
    for clase in ['apta', 'no_apta']:
        ruta_clase = os.path.join(carpeta, clase)
        etiqueta = 1 if clase == 'apta' else 0
        for archivo in os.listdir(ruta_clase):
            img_path = os.path.join(ruta_clase, archivo)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (100, 100))
            X.append(img.flatten())
            y.append(etiqueta)
    return np.array(X), np.array(y)

X, y = cargar_imagenes('Proyecto_GC/Imagenes Guayabas (2)/Imagenes Guayabas')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)
print("Precisión:", modelo.score(X_test, y_test))
