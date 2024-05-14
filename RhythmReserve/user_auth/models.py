from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_groups",
        related_query_name="customuser"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_permissions",
        related_query_name="customuser",
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phoneNumber = models.CharField(
        _('phone number'), max_length=15, unique=True)
    spotifyUsername = models.CharField(
        _('spotify username'), max_length=31, blank=True, default='')
    
    card_number = models.CharField(_('card number'), max_length=16, blank=True, null=True, default=None)
    cardholder_name = models.CharField(_('cardholder name'), max_length=255, blank=True, null=True, default=None)
    exp_month = models.CharField(_('expiration month'), max_length=2, blank=True, null=True, default=None)
    exp_year = models.CharField(_('expiration year'), max_length=4, blank=True, null=True, default=None)
    cvv = models.CharField(_('CVV'), max_length=3, blank=True, null=True, default=None)
    zip_code = models.CharField(_('zip code'), max_length=10, blank=True, null=True, default=None)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
    
class PasswordResetRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='password_reset_requests')
    reset_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def generate_reset_code(cls, user):
        reset_code = ''.join(random.choices(string.digits, k=6))
        expiration_time = timezone.now() + timedelta(hours=1)  #code expires in 1 hour
        password_reset_request = cls.objects.create(user=user, reset_code=reset_code, expires_at=expiration_time)
        return password_reset_request.reset_code

    @classmethod
    def verify_reset_code(cls, user, submitted_code):
        try:
            request = cls.objects.filter(user=user, reset_code=submitted_code).latest('created_at')
            if request and not request.is_expired():
                return True
        except cls.DoesNotExist:
            pass
        return False