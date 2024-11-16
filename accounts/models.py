from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Custom user manager para manejar la creación de usuarios usando email como identificador único"""
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado que usa email como identificador único"""
    
    username = models.CharField(
        _('nombre de usuario'),
        max_length=150,
        help_text=_('Requerido. 150 caracteres o menos.'),
    )
    email = models.EmailField(
        _('dirección de correo electrónico'),
        unique=True,
        error_messages={
            'unique': _("Ya existe un usuario con este correo electrónico."),
        },
    )
    age = models.PositiveIntegerField(
        _('edad'),
        default=0,
        blank=True,
        help_text=_('Edad del usuario')
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designa si el usuario puede acceder al admin site.'),
    )
    is_active = models.BooleanField(
        _('activo'),
        default=True,
        help_text=_(
            'Designa si este usuario debe ser tratado como activo. '
            'Desmarca esto en lugar de borrar cuentas.'
        ),
    )
    date_joined = models.DateTimeField(
        _('fecha de registro'),
        default=timezone.now
    )

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'age']

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Envía un email al usuario"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email