from django.db import models
from django.conf import settings
from datetime import datetime, timedelta

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
        return "user {}'s batch of {} chickens on: {}".format(self.user.id, self.amount, str(self.date))

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = 'Is valid'

    def schedule_vaccinations(self):
        for disease in Disease.objects.filter(has_vaccinations=True):
            vaccination = Vaccination.objects.create(
                batch = self,
                disease = disease,
                date_scheduled = self.date+timedelta(days=disease.vaccinate_days_after_birth)
            )
            for i in range(disease.vaccinations_refills):
                vaccination = Vaccination.objects.create(
                    batch = self,
                    disease = disease,
                    date_scheduled = self.date+timedelta(days=(disease.vaccinate_days_after_birth + ((i + 1) * disease.vaccinations_days_between)))
                )

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
