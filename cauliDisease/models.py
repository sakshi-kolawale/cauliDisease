
from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    prediction = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
