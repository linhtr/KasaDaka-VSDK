from django.db import models
from django.conf import settings

from . import KasaDakaUser, Disease

class UsersDiseases(models.Model):
    user = models.ForeignKey(KasaDakaUser, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return "user {} has {} chickens with the disease {}.".format(self.user.id, self.amount, self.disease.name)

    class Meta:
        unique_together = ('user', 'disease')
        verbose_name = 'User Disease'
        verbose_name_plural = 'Users Diseases'
