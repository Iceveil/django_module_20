from django.contrib.auth.models import User
from django.db import models


def user_image_directory_path(instance: "Profile", filename: str):
    return "users/user_{pk}/images/{filename}".format(pk=instance.user.pk, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, max_length=500)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_image_directory_path)


