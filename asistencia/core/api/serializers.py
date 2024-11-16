from rest_framework import serializers

from core.registration.models import Classroom
from core.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        return instance.toJSON()


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

    def to_representation(self, instance):
        return instance.toJSON()