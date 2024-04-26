from typing import Dict, Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from Themis.models import Employee
from Themis.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeBasicInfoSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'name', 'avatar', 'email', 'title', 'expertise')

    def get_title(self, obj):
        return obj.position.title if obj.position else None


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        user_info = {
            'id': getattr(user, 'id', None),
            'name': getattr(user, 'name', None),
            'avatar': user.avatar.url if user.avatar else None,
            'position': user.position.title if user.position else None,
            'expertise': getattr(user, 'expertise', None),
            'email': getattr(user, 'email', None)
        }
        token['user'] = user_info
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        user_info = {
            'id': getattr(self.user, 'id', None),
            'name': getattr(self.user, 'name', None),
            'avatar': self.user.avatar.url if self.user.avatar else None,
            'position': self.user.position.title if self.user.position else None,
            'expertise': getattr(self.user, 'expertise', None),
            'email': getattr(self.user, 'email', None)
        }
        data.update({'user_info': user_info})
        return data
