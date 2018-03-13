from django.db import models
from ..app_one.models import User, UserManager

class Invitation(models.Model):
    accept = models.BooleanField(default=False)
    ignore = models.BooleanField(default=False)
    invitee = models.ForeignKey(User, related_name="was_invited")
    inviter = models.ForeignKey(User, related_name="invited")
