from django.db import models
from django_multitenant.models import TenantModel
from model_utils.models import TimeStampedModel
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteModel

from vending_machine.models.user import User


class Product(TimeStampedModel, SafeDeleteModel, TenantModel):
    _safedelete_policy = HARD_DELETE

    amount_available = models.IntegerField()
    cost = models.IntegerField()

    product_name = models.CharField(max_length=50, null=True)

    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products", null=False
    )

    class Meta:
        db_table = "product"


    def give_change(self, user_deposited, total_amount, amount):
        change = 0
        op_change = []
        allowed_change = [100, 50, 20, 10, 5]
        if user_deposited > total_amount:
            change = user_deposited - total_amount

        for ac in allowed_change:
            op = change // ac
            if op > 0:
                op_change.append(ac)
                change -= op * ac

        self.amount_available -= amount
        self.save()
        return op_change
