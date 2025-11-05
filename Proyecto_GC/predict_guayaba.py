import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# =============================
# CARGA DEL MODELO
# =============================
MODEL_PATH = "Proyecto_GC/ml_model_guayaba.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"No se encontró el modelo en: {MODEL_PATH}")

model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Modelo cargado correctamente.")

# Diccionario de clases (ajusta según tu estructura)
CLASSES = ['Apta', 'No apta']

# =============================
# FUNCIÓN DE PREDICCIÓN
# =============================
def predict_guayaba(img_path):
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"No se encontró la imagen en: {img_path}")

    # Preprocesamiento
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predicción
    preds = model.predict(img_array)
    class_idx = np.argmax(preds)
    confidence = float(np.max(preds))

    label = CLASSES[class_idx]
    print(f"[DEBUG] Predicciones: {preds}")
    print(f"Resultado: {label}")
    print(f"Confianza: {confidence * 100:.2f}%")
    return label, confidence


# =============================
# PRUEBA LOCAL
# =============================
if __name__ == "__main__":
    # Cambia esta ruta a la imagen que quieras probar
    img_path = "C:/Users/Admin/Documents/GitHub/ProyectoGC_AulaEspejo/static/uploads/captura_guayaba.jpg"
    label, confidence = predict_guayaba(img_path)
    print(f"\n📊 Resultado final: {label} ({confidence * 100:.2f}%)")
