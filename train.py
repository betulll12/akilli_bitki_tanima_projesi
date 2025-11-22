import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# 1. VERİ KÜMESİ YOLUNU AYARLAMA
# !!! Lütfen bu klasörde GUL, ORKIDE, PAPATYA adında alt klasörler oluşturun 
# ve resimleri bu klasörlerin içine yerleştirin.
DATA_DIR = 'data' 
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 3 
EPOCHS = 3 # Test için düşük tutuldu, isterseniz artırabilirsiniz

# 2. VERİ YÜKLEME VE ARTIRMA (DATA AUGMENTATION)
# Veri artırma (data augmentation) ile modelin daha iyi öğrenmesi sağlanır
datagen = ImageDataGenerator(
    rescale=1./255, # Pikselleri 0-1 arasına ölçekle
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2 # Verinin %20'si doğrulama için ayrıldı
)

# Eğitim verilerini yükle
train_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    classes=['GUL', 'ORKIDE', 'PAPATYA'] # Sınıf isimleri Admin panelindeki ile EŞLEŞMELİ
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

# 3. MODELİ TANIMLAMA (BASİT CNN)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(NUM_CLASSES, activation='softmax') # 3 sınıf için softmax
])

# 4. MODELİ DERLEME VE EĞİTME
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("Model Eğitiliyor...")

history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

# 5. MODELİ KAYDETME (KRİTİK ADIM)
MODEL_FILENAME = 'bitki_tanima_modeli.h5'
model.save(MODEL_FILENAME)
print(f"--- AI Modeli Başarıyla Kaydedildi: {MODEL_FILENAME} ---")