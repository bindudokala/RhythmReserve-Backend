from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import Event model from events_app 
from events_app.models import Event

class VenueUserManager(BaseUserManager):
    def create_venue_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        venue_user = self.model(email=email, **extra_fields)
        venue_user.set_password(password)
        venue_user.save(using=self._db)
        return venue_user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_venue_user(email, password, **extra_fields)

class VenueUser(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this venue user belongs to. A venue user will get all permissions granted to each of their groups.'),
        related_name="venueuser_groups",
        related_query_name="venueuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this venue user.'),
        related_name="venueuser_permissions",
        related_query_name="venueuser",
    )

    venue_name = models.CharField(max_length=255)
    venue_image = models.URLField(max_length=1024, blank=True, null=True)
    location = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = VenueUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_event(self, event_name, event_time, event_location, event_image_url,
                    available_general_admission_tickets, general_admission_price,
                    available_vip_tickets, vip_ticket_price, genre, description):
        # Create a new event associated with this venue user
        return Event.objects.create_event(
            venue_user=self,
            event_name=event_name,
            event_time=event_time,
            event_location=event_location,
            event_image_url=event_image_url,
            available_general_admission_tickets=available_general_admission_tickets,
            general_admission_price=general_admission_price,
            available_vip_tickets=available_vip_tickets,
            vip_ticket_price=vip_ticket_price,
            genre=genre,
            description=description
        )
