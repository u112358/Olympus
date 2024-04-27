from typing import Dict, Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from Olympus import settings
from Themis.models.employee import Employee
from Themis.models.operation import Area
from Themis.models.position import Department, Position
from Themis.models.project import Project, ProjectType, Customer, ProjectStatus, Team


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class EmployeeBasicInfoSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'name', 'avatar', 'email', 'gender', 'employee_number',
                  'area', 'department', 'position', 'expertise')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    # 职位英文到中文的映射字典

    def to_representation(self, instance):
        POSITION_MAP = {
            'project_director': '项目总负责',
            'algorythm_leader': '算法负责人',
            'vision_leader': '视觉负责人',
            'mechanic_leader': '机械负责人',
            'ee_leader': '电控负责人',
            'project_manager': '项目经理',
            'business_manager': '商务经理',
            'algorythm_members': '算法成员',
            'vision_members': '视觉成员',
            'mechanic_members': '机械成员',
            'ee_members': '电控成员',
            'maintenance_members': '维护成员',
            # 添加更多映射关系根据需要
        }

        def create_node(employee, key, title_key, node_type='person'):
            """ 创建单个节点的通用函数 """
            if not employee:
                return None
            return {
                'key': key,
                'type': node_type,
                'data': {
                    'image':settings.HOST+employee.avatar.url if employee.avatar else '',
                    'name': employee.name,
                    'title': POSITION_MAP.get(title_key,
                                              employee.position.title) if employee.position else '未知职位'
                },
                'children': []
            }

        def add_children(parent_node, members_qs, key_prefix, title_key):
            """ 添加子节点列表到父节点 """
            for idx, member in enumerate(members_qs.all(), start=1):
                member_key = f"{key_prefix}_{idx}"
                member_node = create_node(member, member_key, title_key)
                if member_node:
                    parent_node['children'].append(member_node)

        # 配置树结构
        node_structure = [
            ('project_director', None),
            ('algorythm_leader', 'algorythm_members'),
            ('vision_leader', 'vision_members'),
            ('mechanic_leader', 'mechanic_members'),
            ('ee_leader', 'ee_members'),
            ('project_manager', 'maintenance_members'),
            ('business_manager', None)
        ]

        # 构建根节点
        root_key = '0'
        root_employee = getattr(instance, 'project_director', None)
        root_node = create_node(root_employee, root_key, title_key='project_director')



        # 构建子节点和可选的子节点的子列表
        if root_node:
            for index, (leader_field, member_field) in enumerate(node_structure, start=1):
                leader = getattr(instance, leader_field, None)
                leader_key = f"{root_key}_{index}"
                leader_node = create_node(leader, leader_key, title_key=leader_field)
                if leader_node:
                    root_node['children'].append(leader_node)
                    if member_field:
                        members_qs = getattr(instance, member_field, None)
                        if members_qs:
                            add_children(leader_node, members_qs, leader_key, title_key=member_field)

        return root_node


class TeamDetailSerializer(serializers.ModelSerializer):
    project_director = EmployeeBasicInfoSerializer(read_only=True)
    algorythm_leader = EmployeeBasicInfoSerializer(read_only=True)
    vision_leader = EmployeeBasicInfoSerializer(read_only=True)
    mechanic_leader = EmployeeBasicInfoSerializer(read_only=True)
    ee_leader = EmployeeBasicInfoSerializer(read_only=True)
    project_manager = EmployeeBasicInfoSerializer(read_only=True)
    business_manager = EmployeeBasicInfoSerializer(read_only=True)

    algorythm_members = EmployeeBasicInfoSerializer(many=True, read_only=True)
    vision_members = EmployeeBasicInfoSerializer(many=True, read_only=True)
    mechanic_members = EmployeeBasicInfoSerializer(many=True, read_only=True)
    ee_members = EmployeeBasicInfoSerializer(many=True, read_only=True)
    maintenance_members = EmployeeBasicInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    team = TeamTreeSerializer()
    project_type = ProjectTypeSerializer()
    project_status = ProjectStatusSerializer()
    customer = CustomerSerializer()
    area = AreaSerializer()

    class Meta:
        model = Project
        fields = ('code', 'snapshot', 'name', 'area', 'project_type',
                  'project_status', 'customer', 'initiation_date',
                  'completion_date_est', 'team')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        user_info = {
            'id': getattr(user, 'id', None),
            'name': getattr(user, 'name', None),
            'avatar': user.avatar.url if user.avatar else None,
            'position': user.position.title if user.position else None,
            'expertise': getattr(user, 'expertise', None),
            'email': getattr(user, 'email', None)
        }
        token['user'] = user_info
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        user_info = {
            'id': getattr(self.user, 'id', None),
            'name': getattr(self.user, 'name', None),
            'avatar': self.user.avatar.url if self.user.avatar else None,
            'position': self.user.position.title if self.user.position else None,
            'expertise': getattr(self.user, 'expertise', None),
            'email': getattr(self.user, 'email', None)
        }
        data.update({'user_info': user_info})
        return data

