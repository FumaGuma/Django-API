from rest_framework import status
from admissions.models import Major, User, Subject, Application, Approval
from admissions.serializers import (
    MajorSerializer,
    UserSerializer,
    SubjectSerializer,
    ApplicationSerializer,
    ApprovalSerializer,
)
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    # Helper view not meant to be used in the final API
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Subjects(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        return Response(SubjectSerializer(subjects, many=True).data)

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


class Students(APIView):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            students = User.objects.filter(is_superuser=False)
            return Response(UserSerializer(students, many=True).data)
        else:
            return Response("Not admin!", status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


class Admins(APIView):
    def get(self, request):
        if request.user.is_superuser:
            admins = User.objects.filter(is_superuser=True)
            return Response(UserSerializer(admins, many=True).data)
        return Response("Not admin!", status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_superuser:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                # admin = User.objects.create_superuser(email=data['email'], password=data['password'],
                #                                      first_name=data['first_name'], last_name=data['last_name'])
                admin = User.objects.create_superuser(**data)
                if admin:
                    admin.save()
                    return Response("Admin created", status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        "Admin creation failed",
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
            else:
                return Response(serializer.errors)
        else:
            return Response("Not admin!", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.is_superuser:
            if pk:
                try:
                    admin = User.objects.get(pk=pk)
                    if admin.is_superuser:
                        admin.delete()
                        return Response("Admin deleted")
                    else:
                        return Response(
                            "Not an admin ID",
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        )
                except User.DoesNotExist:
                    return Response(
                        "Admin ne postoji!", status=status.HTTP_404_NOT_FOUND
                    )
            else:
                return Response("No pk!", status=status.HTTP_400_BAD_REQUEST)
        return Response("Not admin!", status=status.HTTP_401_UNAUTHORIZED)


class Majors(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                serializer = MajorSerializer(Major.objects.get(pk=pk))
                return Response(serializer.data)
            except Major.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        majors = MajorSerializer(Major.objects.all(), many=True)
        return Response(majors.data)

    def post(self, request):
        if request.user.is_superuser:
            serializer = MajorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response("Not logged as admin!", status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.is_superuser:
            if pk:
                try:
                    major = Major.objects.get(pk=pk)
                    major.delete()
                    serializer = MajorSerializer(Major.objects.all(), many=True)
                    return Response(serializer.data)
                except Major.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("No pk!", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response("Not logged as admin!", status=status.HTTP_401_UNAUTHORIZED)


class Applications(APIView):
    def get(self, request):
        if request.user.is_superuser:
            students = User.objects.filter(is_superuser=False)
            applications = Application.objects.filter(student__in=students)
            return Response(ApplicationSerializer(applications, many=True).data)
        else:
            return Response(
                "User is not an admin!", status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request):
        if request.user.is_superuser:
            return Response(
                "Cannot apply, you have an admin account!",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if request.user.enrolled_major:
            return Response(
                "Cannot apply, you are already enrolled in a major!",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if request.user.is_authenticated:
            data = request.data
            major = Major.objects.get(pk=data["major"])
            if major.occupancy >= major.quota:
                return Response(
                    "Cannot apply, quota is filled!", status=status.HTTP_200_OK
                )
            if type(data) != type({}):
                data._mutable = True
            data["student"] = request.user.id
            serializer = ApplicationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


def update_major_occupancies():
    majors = Major.objects.all()
    for major in majors:
        major.occupancy = len(User.objects.filter(enrolled_major=major))
        major.save()


class Approvals(APIView):
    def get(self, request):
        if request.user.is_superuser:
            approvals = Approval.objects.all()
            return Response(ApprovalSerializer(approvals, many=True).data)
        else:
            return Response(
                "User is not an admin!", status=status.HTTP_401_UNAUTHORIZED
            )

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            application_id = request.data["application_id"]
            explanation = request.data["explanation"]
            application = Application.objects.get(pk=application_id)
            student = application.student
            if not student.enrolled_major:
                application.approved = True
                application.save()
                student.enrolled_major = application.major
                student.save()
                update_major_occupancies()
                approval = Approval(
                    explanation=explanation, admin=request.user, student=student
                )
                approval.save()
                return Response(
                    UserSerializer(student).data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    "Student is already enrolled in a major!",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response("User is not admin!", status=status.HTTP_401_UNAUTHORIZED)
