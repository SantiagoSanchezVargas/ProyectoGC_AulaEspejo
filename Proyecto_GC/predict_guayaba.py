import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Cargar el modelo
MODEL_PATH = "ml_model_guayaba_v3.h5"
model = load_model(MODEL_PATH)

# Mapear índices de salida a etiquetas
class_indices = {0: "Apta", 1: "No_Apta"}

def predict_guayaba(img_path):
    """
    Recibe la ruta de una imagen y devuelve:
    - label: 'Apta' o 'No_Apta'
    - confidence: probabilidad de la clase predicha
    """
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # batch de 1

    # Predicción
    preds = model.predict(img_array)
    idx = np.argmax(preds[0])
    label = class_indices[idx]
    confidence = preds[0][idx]

    # DEBUG
    print(f"[DEBUG] Predicción bruta: {preds[0]}, etiqueta: {label}, confianza: {confidence:.4f}")
    
    return label, confidence

# Test rápido desde consola
if __name__ == "__main__":
    ruta_prueba = "C:/Users/Admin/Downloads/TS3B3D3JBNG6DK3X7MMFKN3HFA.jpg"
    label, conf = predict_guayaba(ruta_prueba)
    print(f"Resultado: {label}")
    print(f"Confianza: {conf * 100:.2f}%")
