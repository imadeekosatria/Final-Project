from django.contrib import admin
from .models import Berita, Ringkasan
# Register your models here.


class BeritaAdmin(admin.ModelAdmin):
    list_display = ['judul', 'created']

class RingkasanAdmin(admin.ModelAdmin):
    list_display= ['judul', 'iteration', 'particle', 'timelapsed', 'total_sebelum', 'total_sesudah','created']
    list_filter= ['iteration', 'particle', 'created']

admin.site.register(Berita, BeritaAdmin)
admin.site.register(Ringkasan, RingkasanAdmin)