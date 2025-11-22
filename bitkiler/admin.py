from django.contrib import admin
from .models import Bitki
# Register your models here.
@admin.register(Bitki)
class BitkiAdmin(admin.ModelAdmin):
    list_display = ('isim', 'bilimsel_isim', 'sulama', 'isik')
    search_fields = ('isim', 'bilimsel_isim')

