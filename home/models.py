from django.db import models
from .helpers import generate_slug
from froala_editor.fields import FroalaField

from django.contrib.auth.models import User


class BlogModel(models.Model):
    title = models.CharField(max_length=200)
    content = FroalaField()
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=700, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)
