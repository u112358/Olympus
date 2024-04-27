import re

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from Themis.models.operation import Area
from Themis.models.position import Position, Department, PositionLevel
from Themis.models.project import Project


class Gender(models.TextChoices):
    MALE = "男", _("男")
    FEMALE = "女", _("女")
    UNDISCLOSED = "未知", _("未知")


class City(models.TextChoices):
    DONGGUAN = "东莞", _("东莞")
    HEFEI = "合肥", _("合肥")
    SUZHOU = "苏州", _("苏州")
    GUANGZHOU = "广州", _("广州")
    CHENGDU = "成都", _("成都")
    SHENZHEN = "深圳", _("深圳")


class Status(models.TextChoices):
    ZHENGSHI = "正式", _("正式")
    SHIYONGQI = "试用期", _("试用期")


class Degree(models.Model):
    degree = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.degree}'


class Employee(AbstractUser):
    class Meta:
        verbose_name = _("员工")
        verbose_name_plural = _("员工")

    def validate_phone_number(value):
        phone_regex = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_regex.match(value):
            raise ValidationError(
                "Invalid phone number format. Phone number must be entered in the format: '1234567890'. Up to 15"
                "digits allowed.",
                code='invalid'
            )

    name = models.CharField(_("员工姓名"), max_length=30, null=False)
    employee_number = models.CharField(_("员工工号"), max_length=20, null=False, blank=True)
    area = models.ForeignKey(Area, verbose_name=_("区域"), null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, verbose_name=_("部门"), null=True, blank=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(Position, verbose_name=_("职位"), null=True, blank=True, on_delete=models.SET_NULL)
    position_level = models.ForeignKey(PositionLevel, verbose_name=_("职级"), null=True, blank=True, on_delete=models.SET_NULL)
    date_joined = models.DateField(_("入职时间"), default=timezone.now, blank=True)
    _salary = models.DecimalField(_("薪资"), max_digits=10, decimal_places=2, null=True, blank=True)
    salary_place = models.CharField(_("薪资地"), max_length=40, choices=City.choices, null=True, blank=True)
    work_place = models.CharField(_("工作地"), max_length=40, choices=City.choices, null=True, blank=True)
    contract_place = models.CharField(_("合同地"), max_length=40, choices=City.choices, null=True, blank=True)
    contract_renewed_times = models.SmallIntegerField(_("续签次数"), null=False, default=0)
    contract_start_date = models.DateField(_("合同开始日期"), null=True, blank=True)
    contract_end_date = models.DateField(_("合同结束日期"), null=True, blank=True)
    insurance_place = models.CharField(_("保险地"), choices=City.choices, max_length=40, null=True, blank=True)
    bank_number = models.CharField(_("银行卡号"), max_length=30, null=True, blank=True)
    bank_address = models.CharField(_("银行卡地址"), max_length=40, null=True, blank=True)
    gender = models.CharField(_("性别"), max_length=2, choices=Gender.choices, default=Gender.UNDISCLOSED)
    status = models.CharField(_("状态"), choices=Status.choices, max_length=20, null=True, blank=True)
    expertise = models.CharField(_("专长"), max_length=300, null=True, blank=True)
    avatar = models.ImageField(_("头像"), upload_to="avatars/", null=True, blank=True, default="avatars/default.png")
    phone = models.CharField(_("手机号码"), max_length=17, validators=[validate_phone_number],
                             help_text=_("请按格式输入手机号码：‘1234567890’"))
    id_number = models.CharField(_("身份证号码"), max_length=18, unique=True, null=True, blank=True)
    id_address = models.CharField(_("身份证地址"), max_length=200, null=True, blank=True)
    graduated_from = models.CharField(_("毕业院校"), max_length=30, null=True, blank=True)
    degree = models.ForeignKey(Degree, verbose_name=_("学历"), null=True, blank=True, on_delete=models.SET_NULL)
    watching_projects = models.ManyToManyField(Project, verbose_name=_("关注的项目"), related_name="watching_projects")
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."),
        related_name="employee_groups",
        related_query_name="employee",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="employee_permissions",
        related_query_name="employee",
    )

    def __str__(self):
        return f'{self.name}'

    # name = models.CharField(_("员工姓名"), max_length=30, null=False)
    # employee_number = models.CharField(max_length=20, null=False, blank=True, verbose_name=_("员工工号"))
    # area = models.ForeignKey(OA, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("区域"))
    # department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL, )
    # position = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("职位"))
    # position_level = models.ForeignKey(PositionLevel, null=True, on_delete=models.SET_NULL,
    #                                    verbose_name=_("职级"))
    # date_joined = models.DateField(default=timezone.now, blank=True, verbose_name=_("入职时间"))
    # _salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("薪资"))
    # salary_place = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("薪资地"))
    # work_place = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("工作地"))
    # contract_place = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("合同地"))
    # contract_renewed_times = models.SmallIntegerField(null=False, default=0, verbose_name=_("续签次数"))
    # contract_start_date = models.DateField(null=True, blank=True, verbose_name=_("合同开始日期"))
    # contract_end_date = models.DateField(null=True, blank=True, verbose_name=_("合同结束日期"))
    # insurance_place = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("保险地"))
    # bank_number = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("银行卡号"))
    # gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.UNDISCLOSED, verbose_name=_("性别"),
    #                           )
    # status = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("状态"))
    # expertise = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("专长"))
    # avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, default="avatars/default.png",
    #                            verbose_name=_("头像"))
    # phone = models.CharField(max_length=17, validators=[validate_phone_number],
    #                          help_text=_("请按格式输入手机号码：‘1234567890’"),
    #                          verbose_name=_("手机号码"))
    # id_number = models.CharField(max_length=18, unique=True, null=True, blank=True, verbose_name=_("身份证号码"))
    # id_address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("身份证地址"))
    # graduated_from = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("毕业院校"))
    # degree = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("学历"))
    #
    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_("groups"),
    #     blank=True,
    #     help_text=_(
    #         _("The groups this user belongs to. A user will get all permissions granted to each of their groups.")),
    #     related_name="employee_groups",
    #     related_query_name="employee",
    # )
    #
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_("user permissions"),
    #     blank=True,
    #     help_text=_(_("Specific permissions for this user.")),
    #     related_name="employee_permissions",
    #     related_query_name="employee",
    # )
