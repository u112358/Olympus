# region Project related models
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from Themis.models.employee import Employee
from Themis.models.operation import OA


class ProjectType(models.Model):
    class Meta:
        verbose_name = _("项目类型")
        verbose_name_plural = _("项目类型")

    type = models.CharField(max_length=200, null=False, verbose_name=_("项目类型"))

    def __str__(self):
        return f'{self.type}'


class ProjectStatus(models.Model):
    class Meta:
        verbose_name = _("项目节点")
        verbose_name_plural = _("项目节点")

    status = models.CharField(max_length=200, null=False, verbose_name=_("项目节点"))
    _order_reserved = models.CharField(max_length=20, null=False, default="-1", verbose_name=_("序号"))

    def __str__(self):
        return f'{self.status}'


class Customer(models.Model):
    class Meta:
        verbose_name = _("客户")
        verbose_name_plural = _("客户")

    name = models.CharField(max_length=50, null=False, verbose_name=_("客户名称"))
    location = models.CharField(max_length=50, null=False, verbose_name=_("客户地点"))

    def __str__(self):
        return f'{self.name}-{self.location}'


class Project(models.Model):
    class Meta:
        verbose_name = _("项目")
        verbose_name_plural = _("项目")

    code = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("项目编号"))
    snapshot = models.ImageField(upload_to="project_snapshot/", null=True, blank=True,
                                 default="project_snapshot/default.png", verbose_name=_("项目快照"))
    name = models.CharField(max_length=200, null=False, verbose_name=_("项目名称"))
    area = models.ForeignKey(OA, null=True, blank=True, on_delete=models.SET_NULL,
                             verbose_name=_("项目运营区域"))
    PM = models.ForeignKey(Employee, related_name="managed_projects", null=True, blank=True, on_delete=models.SET_NULL,
                           verbose_name=_("项目经理"))
    BM = models.ForeignKey(Employee, related_name="contracted_projects", null=True, blank=True,
                           on_delete=models.SET_NULL,
                           verbose_name=_("商务经理"))
    type = models.ForeignKey(ProjectType, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("项目类型"))
    status = models.ForeignKey(ProjectStatus, null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name=_("项目节点"))
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("客户"))

    initiation_date = models.DateField(null=True, blank=True, verbose_name=_("立项日期"))
    completion_date_est = models.DateField(null=True, blank=True, verbose_name=_("预计验收日期"))
    watched_by = models.ManyToManyField(Employee, related_name="watched_projects", verbose_name=_("关注项目"), )

    def save(self, *args, **kwargs):
        if not self.code:  # 仅在项目编号未设置时生成
            print("generating code")
            date_str = self.initiation_date.strftime("%Y%m%d")
            last_project = Project.objects.filter(initiation_date=self.initiation_date, area=self.area).order_by(
                "id").last()
            if last_project and last_project.code:
                last_number = int(last_project.code.split("-")[-1])
                new_number = f"{last_number + 1:03d}"  # 序列号加一
            else:
                new_number = "001"  # 当天第一个项目
                self.code = f"{self.area.OA_code}-{date_str}-{new_number}"

            # 设置结项日期默认值为立项日期后三个月
            if not self.completion_date_est:
                self.completion_date_est = self.initiation_date + timedelta(days=90)

            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.code}-{self.name}'


class Task(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        TODO = "todo", _("待分配")
        IN_PROGRESS = "in-progress", _("进行中")
        PAUSED = "paused", _("已暂停")
        CANCELLED = "cancelled", _("已取消")
        DELAYED = "delayed", _("已逾期")
        COMPLETED = "completed", _("已完成")

    class PRIORITY_CHOICES(models.TextChoices):
        NORMAL = "0", _("普通")
        MEDIUM = "1", _("进行中")
        HIGH = "2", _("已暂停")
        URGENT = "3", _("已取消")

    title = models.CharField(max_length=200, null=False, blank=True, verbose_name=_(""))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices, default="todo", null=False,
                              verbose_name=_(""))
    project = models.ForeignKey(Project, related_name="has_tasks",
                                null=False, blank=True, on_delete=models.CASCADE,
                                verbose_name=_(""))
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES.choices, default="0", null=False)
    DRI = models.ForeignKey(Employee, related_name="be_assigned_tasks", null=True,
                            blank=True, on_delete=models.SET_NULL, verbose_name=_(""))
    allocator = models.ForeignKey(Employee, related_name="assigned_tasks", null=True,
                                  blank=True, on_delete=models.SET_NULL, verbose_name=_(""))
    deadline = models.DateTimeField(null=True, blank=True, verbose_name=_(""))
    completed_time = models.DateTimeField(null=True, blank=True, verbose_name=_(""))
    created_time = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name=_(""))
    tag = models.CharField(max_length=50, null=True, blank=True, verbose_name=_(""))
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name=_(""))
    parent_task = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_(""))

# endregion
