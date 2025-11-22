import tensorflow as tf
import numpy as np
from PIL import Image
import os 
from bitkiprojesi.settings import BASE_DIR 

# GLOBAL DEĞİŞKENLER
MODEL = None

# !!! GÜNCELLENDİ: train.py'deki ['GUL', 'ORKIDE', 'PAPATYA'] sırasına uyuldu !!!
CLASS_NAMES = ['GUL', 'ORKIDE', 'PAPATYA'] 
IMAGE_SIZE = (224, 224) 

def load_ai_model():
    """AI Modelini sadece bir kez yükler."""
    global MODEL
    if MODEL is None:
        try:
            model_file_name = 'bitki_tanima_modeli.h5' 
            model_path = os.path.join(BASE_DIR, model_file_name) 
            
            MODEL = tf.keras.models.load_model(model_path)
            print("--- AI Modeli Başarıyla Yüklendi ---")
        except Exception as e:
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
        # Görüntüyü 0-1 aralığına normalize etme (Eğitimdeki gibi)
        img_array = np.array(img) / 255.0  
        # Modeler için gerekli batch boyutu (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0) 
        
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        
        predicted_class_name = CLASS_NAMES[predicted_class_index]
        
        
        if confidence > 0.35: 
            return predicted_class_name
        else:
            # Model güvenilir bir tahmin yapamadı
            return "Tanımlanamadı"

    except Exception as e:
        print(f"Tahmin sırasında hata oluştu: {e}")
        return "Hata"

# Modeli başlangıçta yüklemeye çalışın
load_ai_model()