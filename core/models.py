import secrets

from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords


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
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.username = f"{self.email.split('@')[0]}" \
                        f"_{secrets.token_urlsafe(3)}"
        return super().save(*args, **kwargs)


class Policy(TimeStampedModel):
    class State(models.TextChoices):
        NEW = "NW"
        QUOTED = "QD"
        ACTIVE = "AT"

    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    premium = models.IntegerField()
    cover = models.IntegerField()
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.NEW
    )
    history = HistoricalRecords()

    def activate(self):
        self.state = self.State.ACTIVE
        self.save()

    @property
    def is_active(self):
        return self.state == self.State.ACTIVE

    def __str__(self):
        return f"{self.customer.email}-{self.premium}-{self.state}"
