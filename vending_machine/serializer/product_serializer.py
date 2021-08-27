from rest_framework.serializers import ModelSerializer

from vending_machine.models import Product
from vending_machine.models.user import User
from vending_machine.serializer.user_serializer import UserSerializer


class ProductSerializer(ModelSerializer):

    seller = UserSerializer(required=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "product_name",
            "cost",
            "amount_available",
            "seller",

        )
