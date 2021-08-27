from django.contrib.auth.models import AbstractUser
from django.db import models
from django_multitenant.models import TenantModel
from django.contrib.postgres.fields import JSONField
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


ROLE_CHOICES = (('buyer', 'Buyer'), ('seller', 'Seller'))

class User(AbstractUser, SafeDeleteModel, TenantModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    deposit = models.IntegerField(null=True)
    role =  models.CharField(max_length=50, null=False, choices=ROLE_CHOICES)
    settings = JSONField(null=True)
    tenant_id = "tenant"


    class Meta:
        db_table = "auth_user"
