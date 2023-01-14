from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Profile(models.Model):
    date_of_birth = models.DateField()
    personal_identification = models.CharField(max_length=50)


class User(AbstractUser):
    email_validator = EmailValidator()

    is_customer = models.BooleanField(default=False)
    email = models.CharField(max_length=150, unique=True,
                             validators=[email_validator])
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,
                                   blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Policy(TimeStampedModel):
    class State(models.TextChoices):
        NEW = "NW"
        QUOTED = "QD"
        ACTIVE = "AT"

    premium = models.IntegerField()
    cost = models.IntegerField()
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.NEW
    )
