# Proyecto_GC/predict_guayaba.py
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# --- Cargar modelo ---
MODEL_PATH = 'ml_model_guayaba_v2.h5'
model = load_model(MODEL_PATH)

# --- Función de predicción ---
def predict_guayaba(img_path):
    """
    Recibe la ruta de una imagen, la procesa y devuelve:
    - resultado: 'Apta' o 'No apta'
    - confianza: probabilidad de la clase predicha
    """
    # Cargar y redimensionar imagen
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0            # Normalizar
    img_array = np.expand_dims(img_array, axis=0)  # Agregar batch

    # Predicción
    pred = model.predict(img_array)[0][0]

    # Convertir a etiqueta
    if pred >= 0.5:
        resultado = 'Apta'
        confianza = pred
    else:
        resultado = 'No apta'
        confianza = 1 - pred

    # Debug opcional
    print(f"[DEBUG] Predicción bruta: {pred}, resultado: {resultado}, confianza: {confianza:.4f}")

    return resultado, confianza
