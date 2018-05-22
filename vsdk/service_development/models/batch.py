from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
import math
from .user import *
from .disease import *
from .vaccination import *

class Batch(models.Model):
    user = models.ForeignKey(
        KasaDakaUser,
        verbose_name = 'User',
        on_delete = models.SET_NULL,
        null  = True,
        blank = False,
    )

    date = models.DateField(
        null  = False,
        blank = False,
    )

    amount = models.IntegerField(default = 0)

    def __str__(self):
        return "user {}'s {} batch".format(self.user.id, self.get_user_batch_index_ord())

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = 'Is valid'

    def schedule_vaccinations(self):
        for disease in Disease.objects.filter(has_vaccinations=True):

            # make the first vaccination
            vaccination = Vaccination.objects.create(
                batch = self,
                disease = disease,
                date_scheduled = self.date+timedelta(days=disease.vaccinate_days_after_birth)
            )

            # generate the refill vaccinations
            for i in range(disease.vaccinations_refills):
                vaccination = Vaccination.objects.create(
                    batch = self,
                    disease = disease,
                    date_scheduled = self.date+timedelta(days=(disease.vaccinate_days_after_birth + ((i + 1) * disease.vaccinations_days_between)))
                )

    def get_user_batch_index(self):
        index = 1
        for batch in Batch.objects.filter(user=self.user).order_by('date'):
            if batch == self:
                return index
            index += 1

    def get_user_batch_index_ord(self):
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])
        return ordinal(self.get_user_batch_index())


    def validator(self):
        """
        Returns a list of problems with this element that would surface when accessing
        through voice.
        """
        errors = []

        return errors

    class Meta:
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
