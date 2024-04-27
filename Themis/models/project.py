from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from Themis.models.operation import Area


class ProjectType(models.Model):
    class Meta:
        verbose_name = _("项目类型")
        verbose_name_plural = _("项目类型")

    type = models.CharField(_("项目类型"), max_length=200, null=False)

    def __str__(self):
        return f'{self.type}'


class ProjectStatus(models.Model):
    class Meta:
        verbose_name = _("项目节点")
        verbose_name_plural = _("项目节点")

    status = models.CharField(_("项目节点"), max_length=200, null=False)
    _order_reserved = models.CharField(_("序号"), max_length=20, null=False, default="-1")

    def __str__(self):
        return f'{self.status}'


class Customer(models.Model):
    class Meta:
        verbose_name = _("客户")
        verbose_name_plural = _("客户")

    name = models.CharField(_("客户名称"), max_length=50, null=False)
    location = models.CharField(_("客户地点"), max_length=50, null=False)

    def __str__(self):
        return f'{self.name}-{self.location}'


class Project(models.Model):
    class Meta:
        verbose_name = _("项目")
        verbose_name_plural = _("项目")

    code = models.CharField(_("项目编号"), unique=True, max_length=50, null=True, blank=True)
    snapshot = models.ImageField(_("项目快照"), upload_to="project_snapshot/", null=True, blank=True,
                                 default="project_snapshot/default.png")
    name = models.CharField(_("项目名称"), max_length=200, null=False)
    area = models.ForeignKey(Area, verbose_name=_("项目运营区域"), null=True, blank=True, on_delete=models.SET_NULL)
    project_type = models.ForeignKey(ProjectType, verbose_name=_("项目类型"), null=True, blank=True,
                                     on_delete=models.SET_NULL)
    project_status = models.ForeignKey(ProjectStatus, verbose_name=_("项目节点"), null=True, blank=True,
                                       on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, verbose_name=_("客户"), null=True, blank=True, on_delete=models.SET_NULL)
    initiation_date = models.DateField(_("立项日期"), null=True, blank=True)
    completion_date_est = models.DateField(_("预计验收日期"), null=True, blank=True)
    team = models.ForeignKey("Team", verbose_name=_("实施团队"), related_name="conducting_projects", null=True,
                             blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if not self.code:  # 仅在项目编号未设置时生成
            if self.initiation_date:
                date_str = self.initiation_date.strftime("%Y%m%d")
            else:
                date_str = "3000/01/01"
            last_project = Project.objects.filter(initiation_date=self.initiation_date,
                                                  area=self.area).order_by("id").last()
            if last_project and last_project.code:
                last_number = int(last_project.code.split("-")[-1])
                new_number = f"{last_number + 1:03d}"  # 序列号加一
            else:
                new_number = "001"  # 当天第一个项目
                self.code = f"{self.area.code}-{date_str}-{new_number}"

            # 设置结项日期默认值为立项日期后三个月
            if not self.completion_date_est:
                self.completion_date_est = self.initiation_date + timedelta(days=90)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.code}-{self.name}'


class Team(models.Model):
    class Meta:
        verbose_name = _("团队")
        verbose_name_plural = _("团队")

    name = models.CharField(_("团队名称"), max_length=200, null=False)

    # level --- 0
    project_director = models.ForeignKey("Employee", verbose_name=_("项目总负责"), related_name="is_director_of_teams",
                                         null=True,
                                         blank=True, on_delete=models.SET_NULL)
    # level --- 1
    algorythm_leader = models.ForeignKey("Employee", verbose_name=_("算法负责人"),
                                         related_name="is_algorythm_leader_of_teams",
                                         null=True, blank=True, on_delete=models.SET_NULL)
    vision_leader = models.ForeignKey("Employee", verbose_name=_("视觉负责人"),
                                      related_name="is_vision_leader_of_teams",
                                      null=True,
                                      blank=True, on_delete=models.SET_NULL)
    mechanic_leader = models.ForeignKey("Employee", verbose_name=_("机械负责人"),
                                        related_name="is_mechanic_leader_of_teams",
                                        null=True, blank=True, on_delete=models.SET_NULL)
    ee_leader = models.ForeignKey("Employee", verbose_name=_("电控负责人"), related_name="is_ee_leader_of_teams",
                                  null=True,
                                  blank=True, on_delete=models.SET_NULL)
    project_manager = models.ForeignKey("Employee", verbose_name=_("项目经理"),
                                        related_name="is_project_manager_of_teams",
                                        null=True,
                                        blank=True, on_delete=models.SET_NULL)
    business_manager = models.ForeignKey("Employee", verbose_name=_("商务经理"),
                                         related_name="is_business_manager_of_teams",
                                         null=True, blank=True, on_delete=models.SET_NULL)

    # level --- 2
    algorythm_members = models.ManyToManyField("Employee", verbose_name=_("算法成员"), blank=True,
                                               related_name="is_algorythm_member_of_teams")
    vision_members = models.ManyToManyField("Employee", verbose_name=_("视觉成员"), blank=True,
                                            related_name="is_vision_member_of_teams")
    mechanic_members = models.ManyToManyField("Employee", verbose_name=_("机械成员"), blank=True,
                                              related_name="is_mechanic_member_of_teams")
    ee_members = models.ManyToManyField("Employee", verbose_name=_("电控成员"), blank=True,
                                        related_name="is_ee_member_of_teams")
    maintenance_members = models.ManyToManyField("Employee", verbose_name=_("运维成员"), blank=True,
                                                related_name="is_maintenance_member_of_teams")

    def __str__(self):
        return f'{self.name}'


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

    title = models.CharField(_("标题"), max_length=200, null=False, blank=True)
    status = models.CharField(_("状态"), max_length=20, choices=STATUS_CHOICES.choices, default="todo", null=False)
    project = models.ForeignKey(Project, verbose_name=_("项目"), related_name="has_tasks", null=False, blank=True,
                                on_delete=models.CASCADE)
    priority = models.CharField(_("优先级"), max_length=20, choices=PRIORITY_CHOICES.choices, default="0", null=False)
    DRI = models.ForeignKey("Employee", verbose_name=_("责任人"), related_name="be_assigned_tasks", null=True,
                            blank=True, on_delete=models.SET_NULL, )
    allocator = models.ForeignKey("Employee", verbose_name=_("发起人"), related_name="assigned_tasks", null=True,
                                  blank=True, on_delete=models.SET_NULL, )
    deadline = models.DateTimeField(_("截止时间"), null=True, blank=True, )
    completed_time = models.DateTimeField(_("完成时间"), null=True, blank=True, )
    created_time = models.DateTimeField(_("创建时间"), null=True, blank=True, default=timezone.now, )
    tag = models.CharField(_("标签"), max_length=50, null=True, blank=True, )
    description = models.TextField(_("任务描述"), max_length=2000, null=True, blank=True, )
    parent_task = models.ForeignKey('self', verbose_name=_("父任务"), null=True, blank=True,
                                    on_delete=models.SET_NULL, )

    def __str__(self):
        return f'{self.pk}'
