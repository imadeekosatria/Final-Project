from django.contrib import admin
from .models import Berita, Ringkasan, Comparison
# Register your models here.


class BeritaAdmin(admin.ModelAdmin):
    list_display = ['judul', 'created']

class RingkasanAdmin(admin.ModelAdmin):
    list_display= ['judul', 'iteration', 'particle', 'mode', 'timelapsed', 'total_sebelum', 'total_sesudah','created']
    list_filter= ['iteration', 'particle', 'created']
    search_fields= ['judul']
    list_per_page= 10

class ComparisonAdmin(admin.ModelAdmin):
    list_display=['judul','kalimat_pso', 'iteration_done_pso', 'timelapsed_pso','kalimat_pfnet', 'iteration_done_pfnet', 'timelapsed_pfnet']
    list_filter= ['created']
    search_fields= ['judul']
    list_per_page= 10

admin.site.register(Berita, BeritaAdmin)
admin.site.register(Ringkasan, RingkasanAdmin)
admin.site.register(Comparison, ComparisonAdmin)