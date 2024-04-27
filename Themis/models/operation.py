from django.db import models
from django.utils.translation import gettext_lazy as _


class Area(models.Model):
    class Meta:
        verbose_name = _("运营区域")
        verbose_name_plural = _("运营区域")

    name = models.CharField(_("运营区域"), max_length=50, null=False)
    # OA_code 在项目编号中用来区分项目所属区域
    code = models.CharField(_("区域代码"), max_length=20, null=False)
    manager = models.ForeignKey("Employee", verbose_name=_("区域经理"), related_name="operating",
                                null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}'
