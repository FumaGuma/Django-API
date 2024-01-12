from rest_framework.test import APITestCase
from rest_framework import status
from admissions.models import User, Application, Major
from admissions.tests.fixtures import generate_admin_and_jwt, generate_student_and_jwt
from admissions.serializers import ApplicationSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File


class ApplicationAPITest(APITestCase):
    def setUp(self):
        generate_admin_and_jwt(self)
        major_data = {"name": "strojarstvo", "quota": "20", "occupancy": "0"}
        self.major = Major.objects.create(**major_data)
        student_data = {
            "email": "test@students.com",
            "password": "12345678",
            "first_name": "Mirko",
            "last_name": "Kovalina",
        }
        self.student = User.objects.create(**student_data)
        file = File(open("diploma", "rb"))
        uploaded_file = SimpleUploadedFile("diploma", file.read())
        application_data = {
            "birthdate": "1995-5-3",
            "birthplace": "Zagreb",
            "previous_school": "Gimnazija",
            "previous_school_diploma": uploaded_file,
            "gpa": "4",
            "final_exams_grade": "5",
            "major": self.major.pk,
            "student": self.student.pk,
        }
        serializer = ApplicationSerializer(data=application_data)
        if serializer.is_valid():
            serializer.save()
        self.application = Application.objects.first()

    def test_get_applications(self):
        response = self.client.get("/applications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_application(self):
        generate_student_and_jwt(self)
        file = File(open("diploma", "rb"))
        uploaded_file = SimpleUploadedFile("diploma", file.read())
        application_data = {
            "birthdate": "1995-5-3",
            "birthplace": "Zagreb",
            "previous_school": "Gimnazija",
            "previous_school_diploma": uploaded_file,
            "gpa": "4",
            "final_exams_grade": "5",
            "major": self.major.pk,
        }
        response = self.client.post(
            "/applications/", application_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Application.objects.filter(birthplace="Zagreb").exists())

    def test_create_application_as_admin(self):
        file = File(open("diploma", "rb"))
        uploaded_file = SimpleUploadedFile("diploma", file.read())
        application_data = {
            "birthdate": "1995-5-3",
            "birthplace": "Zagreb",
            "previous_school": "Gimnazija",
            "previous_school_diploma": uploaded_file,
            "gpa": "4",
            "final_exams_grade": "5",
            "major": self.major.pk,
        }
        response = self.client.post(
            "/applications/", application_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Cannot apply, you have an admin account!")

    def test_create_application_when_major_full(self):
        generate_student_and_jwt(self)
        file = File(open("diploma", "rb"))
        uploaded_file = SimpleUploadedFile("diploma", file.read())
        major_data = {"name": "kemija", "quota": "5", "occupancy": "5"}
        major = Major.objects.create(**major_data)
        application_data = {
            "birthdate": "1995-5-3",
            "birthplace": "Zagreb",
            "previous_school": "Gimnazija",
            "previous_school_diploma": uploaded_file,
            "gpa": "4",
            "final_exams_grade": "5",
            "major": major.pk,
        }
        response = self.client.post(
            "/applications/", application_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Cannot apply, quota is filled!")
