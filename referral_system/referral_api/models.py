from django.contrib.auth.models import AbstractUser
from django.db import models
import string
import random

class User(AbstractUser):
    referral_code = models.CharField(max_length=5, unique=True, blank=True)
    referral_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      

    
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)

    def __str__(self):
        return self.username

    def generate_referral_code(self):
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        while User.objects.filter(referral_code=code).exists():
            code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        return code

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)
