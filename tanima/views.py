from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from bitkiler.models import Bitki
from ai_model_service import predict_image # AI servisimizi çağır
# Create your views here.
def tanima_view(request):
    bitki_bilgisi = None
    hata_mesaji = None

    if request.method == 'POST' and request.FILES.get('bitki_resmi'):
        yuklenen_resim = request.FILES['bitki_resmi']
        fs = FileSystemStorage()
        
        # Resmi media klasörüne kaydet
        filename = fs.save(yuklenen_resim.name, yuklenen_resim)
        resim_path = fs.path(filename) 

        # --- AI Tahmini Yap ---
        ai_tahmini = predict_image(resim_path) 
        
        # Tahmin sonucunu kontrol et
        if ai_tahmini in ["Hata", "Model Yüklenemedi", "Tanımlanamadı"]:
            hata_mesaji = f"Bitki tanımlanamadı veya model sorunu: {ai_tahmini}"
            fs.delete(filename)
            
        else:
            try:
                # Veritabanında AI tahminiyle eşleşen bitkiyi bul
                bitki_bilgisi = Bitki.objects.get(isim=ai_tahmini) 
                bitki_bilgisi.uploaded_url = fs.url(filename) 
                
            except Bitki.DoesNotExist:
                hata_mesaji = f"AI '{ai_tahmini}' olarak tanımladı, ancak bu bitkinin detaylı bilgisi veritabanında bulunmuyor. Lütfen /admin panelinde bu kaydı oluşturun."
                fs.delete(filename)
        
    context = {
        'bitki_bilgisi': bitki_bilgisi,
        'hata_mesaji': hata_mesaji,
    }
    return render(request, 'tanima/anasayfa.html', context)

