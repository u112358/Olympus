from django.db import models
from django.utils.translation import gettext_lazy as _
from Themis.models.operation import  OA
# region  Position related models

class PositionLevel(models.Model):
    class Meta:
        verbose_name = _("职级")
        verbose_name_plural = _("职级")

    level = models.CharField(max_length=5,
                             null=False,
                             verbose_name=_("职级"))
    type = models.CharField(max_length=20,
                            null=False,
                            verbose_name=_("序列"))

    def __str__(self):
        return f'{self.type}{self.level}'


class Department(models.Model):
    class Meta:
        verbose_name = _("部门")
        verbose_name_plural = _("部门")

    area = models.ForeignKey(OA,
                             null=True,
                             blank=True,
                             on_delete=models.SET_NULL,
                             verbose_name=_("区域"))
    department = models.CharField(max_length=100,
                                  null=False,
                                  verbose_name=_("部门"))
    director = models.ForeignKey("Position",
                                 related_name="directing_departments",
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name="主管")
    deputy_director = models.ManyToManyField("Position",
                                             related_name="deputy_directing_departments",
                                             blank=True,
                                             verbose_name=_("副主管"))
    parent_department = models.ForeignKey("self",
                                          related_name="children_departments",
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL,
                                          verbose_name=_("上级部门"))

    def __str__(self):
        return f'{self.area}{self.department}'


class Position(models.Model):
    class Meta:
        verbose_name = _("岗位")
        verbose_name_plural = _("岗位")

    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name=_("部门"))
    title = models.CharField(max_length=30, null=False, verbose_name=_("职位"))

    def __str__(self):
        return f'{self.department}-{self.title}'


# endregion