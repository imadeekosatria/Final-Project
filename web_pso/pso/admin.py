from django.contrib import admin
from .models import Berita, Ringkasan
# Register your models here.


class BeritaAdmin(admin.ModelAdmin):
    list_display = ['judul', 'created']

class RingkasanAdmin(admin.ModelAdmin):
    list_display= ['judul', 'iteration', 'particle', 'mode', 'timelapsed', 'total_sebelum', 'total_sesudah','created']
    list_filter= ['iteration', 'particle', 'created']
    search_fields= ['judul']
    list_per_page= 10

admin.site.register(Berita, BeritaAdmin)
admin.site.register(Ringkasan, RingkasanAdmin)