from django.db import models
from django.urls import reverse
from .helpers import *
from .emails import send_account_activation_email
from froala_editor.fields import FroalaField

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username


class BlogModel(models.Model):
    title = models.CharField(max_length=200)
    content = FroalaField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=700, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default.jpg', upload_to='blog')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_update", kwargs={"slug": self.slug})


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = generate_random_string(30)
            Profile.objects.create(user=instance, token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)
