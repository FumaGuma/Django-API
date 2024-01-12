from rest_framework.test import APITestCase
from rest_framework import status
from admissions.models import Major, Subject
from admissions.serializers import SubjectSerializer
from admissions.tests.fixtures import generate_admin_and_jwt


class SubjectMajorAPITest(APITestCase):
    def setUp(self):
        generate_admin_and_jwt(self)
        major_data = {"name": "strojarstvo", "quota": "20", "occupancy": "0"}
        self.major = Major.objects.create(**major_data)
        subject_data = {
            "name": "Termodinamika 2",
            "description": "Sve o temperaturama",
            "ects_points": "5",
            "major": self.major.pk,
        }
        serializer = SubjectSerializer(data=subject_data)
        if serializer.is_valid():
            serializer.save()
        self.subject = Subject.objects.first()

    def test_get_major(self):
        response = self.client.get("/majors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_subject(self):
        response = self.client.get("/subjects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_major(self):
        new_post_data = {"name": "fizika", "quota": "10", "occupancy": "0"}
        response = self.client.post("/majors/", new_post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Major.objects.filter(name="fizika").exists())

    def test_create_subject(self):
        new_post_data = {
            "name": "Termodinamika 4",
            "description": "Još i više o temperaturama",
            "ects_points": "5",
            "major": self.major.pk,
        }
        response = self.client.post("/subjects/", new_post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subject.objects.filter(name="Termodinamika 4").exists())
