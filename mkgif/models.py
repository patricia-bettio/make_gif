from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import django_rq
from .utils import mk_gif_ffmpeg

# Create your models here.

class Animation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    #self, meaning, instance method?
    def enqueue(self, params):
        #enqueue method:
        #a function as a parameter to another function here "mk_gif_ffmpeg"
        django_rq.enqueue(mk_gif_ffmpeg, {
            'pk': self.pk,
            'params': params,
            }
        )

       # print(params)
       # class Meta:
        #    get_latest_by = 'pk'


class Image(models.Model):
    def image_path(self, filename):
        return f'{self.animation.pk}/{filename}'

    animation = models.ForeignKey('Animation', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path)

    #the image properties in html: image.media_url
    @property
    def media_url(self):
        return f'{ settings.MEDIA_URL }{ self.image }'
