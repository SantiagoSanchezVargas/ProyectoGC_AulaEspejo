# predict_guayaba.py
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Cargar modelo entrenado
MODEL_PATH = 'ml_model_guayaba.h5'
model = load_model(MODEL_PATH)

# Diccionario para interpretar la predicción
class_labels = {0: 'No apta', 1: 'Apta'}

def predict_guayaba(img_path):
    """
    img_path: ruta de la imagen a predecir
    retorna: (resultado, probabilidad)
    """
    # Cargar imagen y cambiar tamaño
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalizar
    img_array = np.expand_dims(img_array, axis=0)  # Añadir batch dimension

    # Hacer predicción
    pred = model.predict(img_array)[0][0]

    # Clasificar según umbral 0.5
    label = 1 if pred >= 0.5 else 0

    # DEBUG: imprimir detalles
    print(f"[DEBUG] Predicción bruta: {pred}, etiqueta: {label}, confianza: {pred:.4f}")

    return class_labels[label], float(pred)

# --- Para prueba rápida ---
if __name__ == "__main__":
    img_path = "ruta/a/una_imagen_cualquiera.jpg"  # Cambia esta ruta
    resultado, probabilidad = predict_guayaba(img_path)
    print(f"Resultado: {resultado}")
    print(f"Confianza: {probabilidad * 100:.2f}%")
