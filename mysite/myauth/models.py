from django.contrib.auth.models import User
from django.db import models


# Create your models here.

def profile_avatar_dir_path(instance: 'Profile', filename: str) -> str:
    return "profile/user_{pk}/avatar/{filename}".format(pk=instance.user.pk, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=150, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_dir_path)

    @property
    def active_products(self):
        return self.products.filter(archived=False)
