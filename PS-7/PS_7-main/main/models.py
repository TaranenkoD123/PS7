from django.db import models

# Create your models here.
class Img(models.Model):
    img = models.ImageField('Image')

    def __str__(self):
        return str(self.img)
