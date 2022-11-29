from django.db import models

# Create your models here.
class Berita(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return str(self.name)