from django.db import models
from django.utils.translation import gettext_lazy as _


class OA(models.Model):
    class Meta:
        verbose_name = _("运营区域")
        verbose_name_plural = _("运营区域")

    OA_name = models.CharField(max_length=50, null=False, verbose_name=_("运营区域"))
    # OA_code 在项目编号中用来区分项目所属区域
    OA_code = models.CharField(max_length=20, null=False, verbose_name=_("区域代码"))
    OA_manager = models.ForeignKey("Position", null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name=_("区域经理"))

    def __str__(self):
        return f'{self.OA_name}'
