# Proyecto_GC/ML_model_v2.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- Aumentación de datos ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,          # Rotaciones aleatorias
    width_shift_range=0.1,      # Traslación horizontal
    height_shift_range=0.1,     # Traslación vertical
    zoom_range=0.2,             # Zoom aleatorio
    horizontal_flip=True,       # Volteo horizontal
    validation_split=0.2        # 20% para validación
)

# --- Generadores de entrenamiento y validación ---
train_generator = train_datagen.flow_from_directory(
    'Proyecto_GC/Imagenes',  # Carpeta principal con subcarpetas 'Aptas' y 'No_Aptas'
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training',
    shuffle=True
)

val_generator = train_datagen.flow_from_directory(
    'Proyecto_GC/Imagenes',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='validation',
    shuffle=True
)

# --- Modelo CNN mejorado ---
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),                 # Reduce sobreajuste
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# --- Entrenamiento ---
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=20,                   # Ajusta según tus recursos
    verbose=1
)

# --- Guardar modelo ---
model.save('ml_model_guayaba_v2.h5')
print("Modelo guardado como ml_model_guayaba_v2.h5")
