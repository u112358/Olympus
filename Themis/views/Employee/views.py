from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from Themis.models.employee import Employee
from Themis.models.project import Project
from Themis.serializers import EmployeeSerializer, LoginSerializer, EmployeeBasicInfoSerializer, \
    ProjectSerializer, ProjectDetailSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(APIView):

    def get(self, request, project_id):
        print(project_id)
        project = Project.objects.get(pk=project_id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


@api_view(['GET'])
def employee_basic_info(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    serializer = EmployeeBasicInfoSerializer(employee)
    return Response(serializer.data)


class UploadView(APIView):
    def post(self, request, nid):
        url_path = request.path
        if 'employees' in url_path:
            model = Employee
            file_key = 'avatar'
            model_field = 'avatar'
            serializer = EmployeeSerializer
        elif 'projects' in url_path:
            model = Project
            file_key = 'snapshot'
            model_field = 'snapshot'
            serializer = ProjectSerializer
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = model.objects.get(pk=nid)
        except model.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        if file_key in request.FILES:
            setattr(instance, model_field, request.FILES[file_key])
            instance.save()
            serialized_ins = serializer(instance)
            return Response(serialized_ins.data[file_key], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
