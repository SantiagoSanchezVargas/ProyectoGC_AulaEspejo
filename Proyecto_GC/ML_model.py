import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers
import os

# =============================
# CONFIGURACIÓN BÁSICA
# =============================
BASE_DIR = "Proyecto_GC/Imagenes Guayabas"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15  # puedes ajustar

# =============================
# PREPROCESAMIENTO Y AUGMENTACIÓN
# =============================
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    BASE_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_data = datagen.flow_from_directory(
    BASE_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

print("\n📁 Clases detectadas:", train_data.class_indices)

# =============================
# MODELO
# =============================
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(2, activation='softmax')  # solo dos clases
])

model.compile(
    optimizer=optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# =============================
# ENTRENAMIENTO
# =============================
history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=val_data
)

# =============================
# GUARDAR MODELO
# =============================
os.makedirs("Proyecto_GC", exist_ok=True)
model.save("Proyecto_GC/ml_model_guayaba.h5")

print("\n✅ Modelo entrenado y guardado correctamente.")
