from django.db import models

# Create your models here.
class Bitki(models.Model):
    # Bu isim, AI modelinin döndüreceği tahmin ile EŞLEŞMELİDİR!
    isim = models.CharField(max_length=100, unique=True, verbose_name="Bitki Adı (AI Tahmini)")
    
    bilimsel_isim = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bilimsel Adı")
    
    bakim_bilgisi = models.TextField(verbose_name="Genel Bakım İpuçları")
    
    sulama = models.CharField(max_length=200, verbose_name="Sulama Sıklığı")
    
    isik = models.CharField(max_length=200, verbose_name="Işık İhtiyacı")
    
    gorsel = models.ImageField(upload_to='bitki_gorselleri/', blank=True, null=True, verbose_name="Örnek Görsel")

    def __str__(self):
        return self.isim