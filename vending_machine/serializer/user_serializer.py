from rest_framework.serializers import ModelSerializer

from vending_machine.models.user import User



class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "deposit",
            "role",
            "is_active",
        )
