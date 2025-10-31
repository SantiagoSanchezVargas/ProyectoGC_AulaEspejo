import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = 'ml_model_guayaba.h5'
model = load_model(MODEL_PATH)

class_labels = {0: 'No apta', 1: 'Apta'}

def predict_guayaba(img_path):
    """Predice si una guayaba es apta o no."""
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)
    pred = np.squeeze(pred)  # quita dimensiones extra

    # Si la salida tiene 2 valores → softmax
    if pred.ndim > 0 and pred.shape[-1] == 2:
        label = int(np.argmax(pred))
        confidence = float(pred[label])
    else:
        # Salida sigmoide (una sola neurona)
        label = int(pred >= 0.5)
        confidence = float(pred)

    print(f"[DEBUG] Predicción bruta: {pred}, etiqueta: {label}, confianza: {confidence:.4f}")

    return class_labels[label], confidence