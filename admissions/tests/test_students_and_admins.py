from rest_framework.test import APITestCase
from rest_framework import status
from admissions.models import User
from admissions.tests.fixtures import generate_admin_and_jwt


class StudentAdminAPITest(APITestCase):
    def setUp(self):
        generate_admin_and_jwt(self)
        student_data = {
            "email": "test@students.com",
            "password": "12345678",
            "first_name": "Mirko",
            "last_name": "Kovalina",
        }
        self.student = User.objects.create(**student_data)

    def test_get_students(self):
        response = self.client.get("/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_student(self):
        student_data = {
            "email": "new_student@students.com",
            "password": "12345678",
            "first_name": "Robert",
            "last_name": "Gradeon",
        }
        response = self.client.post("/students/", student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new_student@students.com").exists())

    def test_create_invalid_email(self):
        student_data = {
            "email": "new_student",
            "password": "12345678",
            "first_name": "Robert",
            "last_name": "Gradeon",
        }
        response = self.client.post("/students/", student_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(User.objects.filter(email="new_student").exists())

    def test_create_admin(self):
        admin_data = {
            "email": "bob@admin.com",
            "password": "12345678",
            "first_name": "Bob",
            "last_name": "Konstrakt",
        }
        response = self.client.post("/admins/", admin_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="bob@admin.com").exists())

    def test_delete_admin(self):
        admin_data = {
            "email": "bob@admin.com",
            "password": "12345678",
            "first_name": "Bob",
            "last_name": "Konstrakt",
        }
        response = self.client.post("/admins/", admin_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="bob@admin.com"))
        user = User.objects.filter(email="bob@admin.com").first()
        response = self.client.delete(f"/admins/{user.pk}")
        self.assertFalse(User.objects.filter(email="bob@admin.com").exists())
