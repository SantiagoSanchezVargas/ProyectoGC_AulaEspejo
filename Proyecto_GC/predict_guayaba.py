# predict_guayaba.py (versión para ml_model_guayaba_v2.h5)
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# --- Cargar modelo mejorado ---
MODEL_PATH = 'ml_model_guayaba_v2.h5'
model = load_model(MODEL_PATH)

# --- Diccionario para interpretación ---
class_labels = {0: 'No apta', 1: 'Apta'}

def predict_guayaba(img_path):
    """
    Realiza la predicción sobre una imagen dada.
    Retorna: ('Apta'/'No apta', confianza)
    """
    # Cargar imagen y preprocesar
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)  # Usa el preprocesamiento específico de MobileNetV2
    img_array = np.expand_dims(img_array, axis=0)

    # Predicción
    pred = model.predict(img_array)[0][0]
    label = 1 if pred >= 0.5 else 0

    print(f"[DEBUG] Predicción bruta: {pred}, etiqueta: {label}, confianza: {pred:.4f}")
    return class_labels[label], float(pred)

# --- Bloque de prueba ---
if __name__ == "__main__":
    img_path = "ruta/a/una_imagen_cualquiera.jpg"  # ⚠️ Cambia por la ruta real de una imagen
    label, confidence = predict_guayaba(img_path)
    print(f"Resultado: {label}")
    print(f"Confianza: {confidence * 100:.2f}%")
