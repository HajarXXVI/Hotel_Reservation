from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # LANGUAGE_CHOICES = [
    #     ('en', _('English')),
    #     ('fr', _('French')),
    #     ('ar', _('Arabic')),
    # ]

    username = None  # Remove username field for email-only authentication
    
    email = models.EmailField(
        _('email address'),
        max_length=150,  # Reduced length
        unique=True,
        db_index=True  # Explicit index
    )
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    address = models.TextField(_('address'), blank=True)
    # date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    # profile_picture = models.ImageField(
    #     upload_to='profile_pictures/',
    #     null=True,
    #     blank=True
    # )
    
    # Make email the required field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
