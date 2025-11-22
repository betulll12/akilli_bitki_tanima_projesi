import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping # YENİ EKLEME
import os

# 1. VERİ KÜMESİ YOLUNU AYARLAMA
DATA_DIR = 'data' 
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 3 
EPOCHS = 30 

# 2. VERİ YÜKLEME VE ARTIRMA (DATA AUGMENTATION)
datagen = ImageDataGenerator(
    rescale=1./255, 
    rotation_range=30, 
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2 
)

# Eğitim verilerini yükle
train_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    classes=['GUL', 'ORKIDE', 'PAPATYA']
)

# Doğrulama verilerini yükle
validation_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    classes=['GUL', 'ORKIDE', 'PAPATYA']
)

# 3. MODELI TANIMLAMA (DAHA DERIN CNN)
model = Sequential([
    Conv2D(64, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(256, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dropout(0.5), 
    Dense(512, activation='relu'), 
    Dense(NUM_CLASSES, activation='softmax')
])

# 4. MODELİ DERLEME VE EĞİTME
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# ERKEN DURDURMA OLUŞTURULDU (YENİ EKLEME)
# Doğrulama kaybı 5 epoch boyunca iyileşmezse eğitimi durdur.
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)


print("Model Eğitiliyor...")

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS, 
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=[early_stop] # CALLBACK KULLANILDI
)

# 5. MODELİ KAYDETME
MODEL_FILENAME = 'bitki_tanima_modeli.h5'
model.save(MODEL_FILENAME)
print(f"--- AI Modeli Başarıyla Kaydedildi: {MODEL_FILENAME} ---")