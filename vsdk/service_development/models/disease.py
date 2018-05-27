from django.db import models
from django.conf import settings

from .voicelabel import VoiceLabel
from .disease_vaccinationday import DiseaseVaccinationday

class Disease(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True, null=True)
    voice_label = models.ForeignKey(
            VoiceLabel,
            verbose_name = 'Voice label',
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )
    # has_vaccinations = models.BooleanField(null = False, default = True)
    # # vaccinations_refills = models.IntegerField(null = False, default = 0)
    # # vaccinate_days_after_birth = models.IntegerField(null = False, default = 7)
    # # vaccinations_days_between  = models.IntegerField(null = False, default = 7)

    def __str__(self):
        return self.name

    def has_vaccinations(self):
        return len(DiseaseVaccinationday.objects.filter(disease  = self)) > 0

    def get_vaccination_days(self):
        return DiseaseVaccinationday.objects.filter(disease = self)

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
        #check if voice label is present, and validate it
        if self.voice_label:
            for language in self.service.supported_languages.all():
                errors.extend(self.voice_label.validator(language))
        else:
            errors.append(ugettext('No VoiceLabel in: "%s"')%str(self))
        return errors

    def get_voice_fragment_url(self, language):
        """
        Returns the url of the audio file of this element, in the given language.
        """
        return self.voice_label.get_voice_fragment_url(language)

    class Meta:
        verbose_name = 'Disease'
        verbose_name_plural = 'Diseases'
