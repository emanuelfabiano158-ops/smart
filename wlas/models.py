from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.conf import settings


# =========================
# USER MANAGER
# =========================
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        return self.create_user(email, password, **extra_fields)


# =========================
# CUSTOM USER
# =========================
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("bsf_keeper", "BSF Keeper"),
        ("viewer", "Viewer"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")

    # ✅ FIX: avoid Django auth conflict
    groups = models.ManyToManyField(
        Group,
        related_name="bsf_custom_users",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="bsf_custom_user_permissions",
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"


# =========================
# CONTACTS (for alerts)
# =========================
class Contact(models.Model):
    CONTACT_TYPES = [
        ("email", "Email"),
        ("phone", "Phone"),
        ("whatsapp", "WhatsApp"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contacts"
    )

    type = models.CharField(max_length=20, choices=CONTACT_TYPES)
    value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.type}"


# =========================
# CONTAINERS (BSF SITE UNITS)
# =========================
class Container(models.Model):
    label = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=255, blank=True)

    max_depth = models.FloatField(help_text="Maximum depth in cm")

    alert_min = models.FloatField(null=True, blank=True)
    alert_max = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label


# =========================
# SENSOR DEVICE
# =========================
class Sensor(models.Model):
    SENSOR_TYPES = [
        ("ultrasonic", "Ultrasonic"),
        ("float", "Float"),
        ("other", "Other"),
    ]

    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
        related_name="sensors"
    )

    type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    status = models.CharField(max_length=20, default="active")
    installed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.container.label}"


# =========================
# WATER LEVEL DATA (TIME SERIES)
# =========================
class WaterLevel(models.Model):
    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
        related_name="water_levels"
    )

    depth = models.FloatField(help_text="Water depth in cm")
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.container.label} - {self.depth} cm"


# =========================
# ALERT SYSTEM
# =========================
class Alert(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE)

    message = models.TextField()
    level = models.FloatField()
    triggered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert - {self.container.label}"