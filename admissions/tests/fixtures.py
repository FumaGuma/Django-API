from admissions.models import User
from django.contrib.auth.hashers import make_password
from admissions.serializers import UserSerializer


def generate_admin_and_jwt(APITestCase):
    APITestCase.admin_data = {
        "email": "admin@admin.com",
        "password": "12345678",
        "first_name": "Minda",
        "last_name": "Nimad",
    }
    APITestCase.admin = User.objects.create_superuser(**APITestCase.admin_data)
    token_post_data = {"email": "admin@admin.com", "password": "12345678"}
    response = APITestCase.client.post("/api/token/", token_post_data, format="json")
    APITestCase.admin_jwt = response.data["access"]
    APITestCase.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
    )


def generate_student_and_jwt(APITestCase):
    APITestCase.student_data = {
        "email": "prudent@student.com",
        "password": "12345678",
        "first_name": "Dentstu",
        "last_name": "Nutdest",
    }
    serializer = UserSerializer(data=APITestCase.student_data)
    if serializer.is_valid():
        serializer.save()
    APITestCase.student = User.objects.last()
    token_post_data = {"email": "prudent@student.com", "password": "12345678"}
    response = APITestCase.client.post("/api/token/", token_post_data, format="json")
    APITestCase.student_jwt = response.data["access"]
    APITestCase.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
    )
