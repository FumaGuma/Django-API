from rest_framework import serializers
from admissions.models import Major, User, Subject, Application, Approval
from django.contrib.auth.hashers import make_password


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class MajorSerializer(serializers.ModelSerializer):
    subject_set = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Major
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    enrolled_major = MajorSerializer(read_only=True)
    email = serializers.EmailField()

    def validate_password(self, value: str) -> str:
        return make_password(value)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "enrolled_major",
            "is_superuser",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


class ApprovalSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Approval
        fields = "__all__"
