from django.db import models
from django.conf import settings

class DiseaseVaccinationday(models.Model):
    disease = models.ForeignKey("Disease", on_delete=models.CASCADE)
    number = models.IntegerField(null = False)
    days_after_birth = models.IntegerField(null = False)

    def __str__(self):
        return "{} days after birth for {}.".format(self.days_after_birth, self.disease.name)

    class Meta:
        verbose_name = 'Disease Vaccination Day'
        verbose_name_plural = 'Disease Vaccination Days'
