from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# --- Preparación de datos ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    'Proyecto_GC/Imagenes Guayabas (2)/Imagenes Guayabas',  # carpeta con subcarpetas 'apta' y 'no_apta'
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    'dataset_guayabas',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

# --- Modelo CNN básico ---
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# --- Entrenamiento ---
model.fit(train_generator, validation_data=val_generator, epochs=15)

# --- Guardar modelo ---
model.save('ml_model_guayaba.h5')
print("Modelo guardado como ml_model_guayaba.h5")
