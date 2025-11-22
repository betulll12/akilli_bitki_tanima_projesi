# tanima/ai_model_service.py

import tensorflow as tf
import numpy as np
from PIL import Image
import os # BASE_DIR kullanmak için eklendi
from bitkiprojesi.settings import BASE_DIR # BASE_DIR ayar dosyasından çekildi

# GLOBAL DEĞİŞKENLER
MODEL = None

# !!! BURAYI SİZİN MODELİNİZİN SINIF İSİMLERİYLE GÜNCELLEYİNİZ !!!
# NOT: Bu isimler, Admin panelindeki bitki isimleriyle TAM EŞLEŞMELİDİR.
CLASS_NAMES = ['ORKIDE', 'PAPATYA', 'GÜL'] 
IMAGE_SIZE = (224, 224) 

def load_ai_model():
    """AI Modelini sadece bir kez yükler."""
    global MODEL
    if MODEL is None:
        try:
            # !!! BURAYI KENDİ MODELİNİZİN YOLU İLE GÜNCELLEYİNİZ !!!
            # Model dosyanızın projenin ana klasöründe olduğunu varsayarak:
            # Örnek: 'bitki_tanima_modeli.h5'
            model_file_name = 'bitki_tanima_modeli.h5' # <--- Modelinizin adını buraya yazın
            model_path = os.path.join(BASE_DIR, model_file_name) 
            
            # Eğer modeliniz başka bir klasördeyse, yolu buna göre düzenleyin.
            # model_path = os.path.join(BASE_DIR, 'modeller', model_file_name)
            
            MODEL = tf.keras.models.load_model(model_path)
            print("--- AI Modeli Başarıyla Yüklendi ---")
        except Exception as e:
            # Hata mesajını daha anlaşılır hale getiriyoruz
            print(f"AI Model yüklenirken hata oluştu: {e}. Kontrol Edilen Yol: {model_path}. Lütfen model yolunu kontrol edin.")
            MODEL = None
    return MODEL

def predict_image(image_path):
    """Verilen resim yolunu kullanarak tahminde bulunur."""
    model = load_ai_model()
    if model is None:
        return "Model Yüklenemedi"

    try:
        img = Image.open(image_path).convert('RGB').resize(IMAGE_SIZE) 
        img_array = np.array(img) / 255.0  
        img_array = np.expand_dims(img_array, axis=0) 
        
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        
        predicted_class_name = CLASS_NAMES[predicted_class_index]
        
        if confidence > 0.70: # %70 güven eşiği
            return predicted_class_name
        else:
            return "Tanımlanamadı"

    except Exception as e:
        print(f"Tahmin sırasında hata oluştu: {e}")
        return "Hata"

# Modeli başlangıçta yüklemeye çalışın
load_ai_model()

