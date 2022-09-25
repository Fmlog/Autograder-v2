from rest_framework import serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'login_id', 'password', "role")
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'write_only': True},
        }

    def create (self, validated_data):
        """
        Validates new user data on Registration.
        
        :param validated_data: Auto-validated request (creation) data
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
