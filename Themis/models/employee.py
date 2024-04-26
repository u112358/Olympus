import re

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from Themis.models.position import Position, PositionLevel


class Gender(models.TextChoices):
    MALE = "M", _("男")
    FEMALE = "F", _("女")
    NON_BINARY = "NB", _("Non-binary")
    UNDISCLOSED = "U", _("Prefer not to disclose")


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

    name = models.CharField(max_length=30, null=False, verbose_name=_("员工姓名"))
    employee_number = models.CharField(max_length=20, null=False, blank=True, verbose_name=_("员工工号"))
    position = models.ForeignKey(Position, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("职位"))
    position_level = models.ForeignKey(PositionLevel, null=True, on_delete=models.SET_NULL,
                                       verbose_name=_("职级"))
    date_joined = models.DateField(default=timezone.now, blank=True, verbose_name=_("入职时间"))
    # director = models.ForeignKey(_("self"), on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("直接领导"))
    _salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("薪资"))
    salary_place = models.CharField(max_length=40, null=True, blank=True)
    work_place = models.CharField(max_length=40, null=True, blank=True)
    contract_place = models.CharField(max_length=40, null=True, blank=True)
    contract_renewed_times = models.SmallIntegerField(null=False, default=0)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    insurance_place = models.CharField(max_length=40, null=True, blank=True)
    bank_number = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(
        max_length=2,
        choices=Gender.choices,
        default=Gender.UNDISCLOSED,
        verbose_name=_("Gender"),
    )
    status = models.CharField(max_length=20, null=True, blank=True)
    expertise = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("专长"))
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, default="avatars/default.png",
                               verbose_name=_("头像"))
    phone = models.CharField(max_length=17, validators=[validate_phone_number],
                             help_text=_("请按格式输入手机号码：‘1234567890’"),
                             verbose_name=_("手机号码"))
    id_number = models.CharField(max_length=18, unique=True, null=True, blank=True, verbose_name=_("id number"))
    id_address = models.CharField(max_length=200, null=True, blank=True)
    graduated_from = models.CharField(max_length=30, null=True, blank=True)
    degree = models.CharField(max_length=30, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_(_("groups")),
        blank=True,
        help_text=_(
            _("The groups this user belongs to. A user will get all permissions granted to each of their groups.")),
        related_name="employee_groups",  # 自定义的 related_name
        related_query_name="employee",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_(_("user permissions")),
        blank=True,
        help_text=_(_("Specific permissions for this user.")),
        related_name="employee_permissions",  # 自定义的 related_name
        related_query_name="employee",
    )

    def __str__(self):
        return f'{self.name}-{self.employee_number}'
