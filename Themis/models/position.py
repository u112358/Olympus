from django.db import models
from django.utils.translation import gettext_lazy as _


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

    name = models.CharField(_("部门"), max_length=100, null=False)
    parent_department = models.ForeignKey("self", verbose_name=_("上级部门"),
                                          related_name="children_departments",
                                          null=True,
                                          blank=True, on_delete=models.SET_NULL
                                          )

    def __str__(self):
        return f'{self.name}'


class Position(models.Model):
    class Meta:
        verbose_name = _("岗位")
        verbose_name_plural = _("岗位")

    title = models.CharField(_("职位"), max_length=30, null=False, )

    def __str__(self):
        return f'{self.title}'
