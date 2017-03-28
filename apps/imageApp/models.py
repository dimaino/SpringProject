from __future__ import unicode_literals
from django.db import models

class ImageModel(models.Model):
    model_pic = models.ImageField(upload_to = 'apps/imageApp/static/imageApp/images/', default = 'apps/imageApp/static/imageApp/images/no-img.jpg')
