import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone

from .batch import *
from .disease import *

class Vaccination(models.Model):
    batch = models.ForeignKey(
        Batch,
        verbose_name = 'Batch',
        on_delete = models.SET_NULL,
        null  = True,
        blank = False,
    )
    disease = models.ForeignKey(
        Disease,
        verbose_name = 'Disease',
        on_delete = models.SET_NULL,
        null  = True,
        blank = False,
    )

    date_scheduled = models.DateField(
        null  = False,
        blank = False,
    )
    date_given = models.DateField(
        null  = True,
        blank = True,
    )

    amount = models.IntegerField(default = 0)

    def __str__(self):
        return "vaccination {}".format(self.id)

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = 'Is valid'

    def validator(self):
        """
        Returns a list of problems with this element that would surface when accessing
        through voice.
        """
        errors = []

        return errors

    def get_due_date(date):
        return self.filter(date_scheduled = date)

    def get_due_today():
        return get_due_date(datetime.date.today())

    def has_been_given():
        return self.date_given <= datetime.date.today()

    class Meta:
        verbose_name = 'Vaccination'
        verbose_name_plural = 'Vaccinations'
