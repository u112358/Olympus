from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from Olympus import settings
from django.contrib import admin
from Themis.views.Employee.views import EmployeeViewSet, LoginView, UploadView, employee_basic_info, ProjectViewSet, \
    ProjectDetailView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/employees/<int:nid>/avatar/', UploadView.as_view(), name='upload_avatar'),
    path('api/projects/<int:nid>/snapshot/', UploadView.as_view(), name='upload_snapshot'),
    path('api/employees/<int:employee_id>/basicInfo/', employee_basic_info, name='employee_basic_info'),
    path('api/projects/<int:project_id>/detail/', ProjectDetailView.as_view(), name='project_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
