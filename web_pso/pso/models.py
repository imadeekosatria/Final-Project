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
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.judul)
