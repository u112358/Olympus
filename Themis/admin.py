from django.contrib import admin

from Themis.models.employee import Employee
from Themis.models.operation import Area
# Register your models here.
from Themis.models.position import Position, Department, PositionLevel
from Themis.models.project import Project, ProjectType, ProjectStatus, Task, Team, Customer


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'department', 'position', 'degree', 'status')
    list_filter = ('area', 'position', 'department')
    list_per_page = 10
    fieldsets = [
        ("员工", {
            'fields': ['name', 'email', 'phone', 'gender',
                       'avatar',
                       'id_number', 'id_address',
                       'graduated_from', 'degree', 'expertise']
        }),
        ("岗位", {
            'fields': (('area', 'department', 'position'),
                       ('status', '_salary'),
                       ('salary_place', 'work_place', 'contract_place', 'insurance_place'))
        }),
    ]


class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ('algorythm_members', 'ee_members', 'mechanic_members',
                         'vision_members', 'maintenance_members')


admin.site.register(Position)
admin.site.register(Department)
admin.site.register(PositionLevel)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Area)
admin.site.register(Project)
admin.site.register(ProjectType)
admin.site.register(ProjectStatus)
admin.site.register(Task)
admin.site.register(Team, TeamAdmin)
admin.site.register(Customer)
