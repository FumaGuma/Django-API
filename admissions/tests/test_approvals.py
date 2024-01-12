from rest_framework.test import APITestCase
from rest_framework import status
from admissions.models import User, Application, Approval, Major
from admissions.tests.fixtures import generate_admin_and_jwt, generate_student_and_jwt
from admissions.serializers import ApplicationSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File


class ApprovalAPITest(APITestCase):
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

    def test_approval(self):
        approval_data = {
            "application_id": self.application.id,
            "explanation": "Student approved!",
        }
        response = self.client.post("/approvals/", approval_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        approval = Approval.objects.first()
        self.assertEqual(approval.explanation, "Student approved!")
        self.assertEqual(approval.student, self.student)
        self.assertEqual(
            approval.student.enrolled_major, self.major
        )  # Check that correct major is enrolled
        self.assertEqual(
            Major.objects.first().occupancy, 1
        )  # Check that the occupancy is adjusted
