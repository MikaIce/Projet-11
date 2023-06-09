from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from pathlib import Path

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

    def save(self, *args, **kwargs):
        if not self.profile_image:
            if self.gender == 'F':
                self.profile_image = 'profile_images/default_female.jpg'
            else:
                self.profile_image = 'profile_images/default_male.jpg'
        else:
            img = Image.open(self.profile_image)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new(img.mode[:-1], img.size, '#FFFFFF')
                background.paste(img, img.split()[-1])
                img = background

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

            output = BytesIO()
            img.save(output, format='JPEG', quality=100)
            output.seek(0)
            self.profile_image = InMemoryUploadedFile(output, 'ImageField',
                "%s.jpg" % self.profile_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        super().save(*args, **kwargs)
