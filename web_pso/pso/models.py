from django.db import models

# Create your models here.
class Berita(models.Model):
    judul = models.CharField(max_length=255, unique=True)
    teks = models.TextField() 
    file = models.FileField(default=None, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return str(self.judul)

    


class Ringkasan(models.Model):
    judul = models.CharField(max_length=255)
    teks_asli = models.TextField()
    ringkasan = models.TextField()
    kalimat = models.CharField(default=None, max_length=255)
    iteration = models.IntegerField(default=None)
    particle = models.IntegerField(default=None)
    timelapsed = models.IntegerField(verbose_name='Time Lapsed (seconds)', default=None)
    total_sebelum = models.IntegerField(default=None)
    total_sesudah = models.IntegerField(default=None)
    mode = models.CharField(max_length=255, default='pso')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.judul)
    
class Comparison(models.Model):
    judul = models.CharField(max_length=255)
    teks_asli = models.TextField()

    #PSO
    ringkasan_pso = models.TextField()
    kalimat_pso = models.CharField(default=None, max_length=255)
    iteration_done_pso = models.IntegerField(default=None)
    iteration_pso = models.IntegerField(default=None)
    particle_pso = models.IntegerField(default=None)
    timelapsed_pso = models.IntegerField(verbose_name='Time Lapsed (seconds)', default=None)
    total_sebelum_pso = models.IntegerField(default=None)
    total_sesudah_pso = models.IntegerField(default=None)

    #PFNet
    ringkasan_pfnet = models.TextField()
    kalimat_pfnet = models.CharField(default=None, max_length=255)
    iteration_done_pfnet = models.IntegerField(default=None)
    iteration_pfnet = models.IntegerField(default=None)
    particle_pfnet = models.IntegerField(default=None)
    timelapsed_pfnet = models.IntegerField(verbose_name='Time Lapsed (seconds)', default=None)
    total_sebelum_pfnet = models.IntegerField(default=None)
    total_sesudah_pfnet = models.IntegerField(default=None)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.judul)

class Testing(models.Model):
    judul = models.CharField(max_length=255, verbose_name='Berita')
    data_json = models.JSONField(verbose_name='JSON', null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    def __str__(self):
        return str(self.judul)