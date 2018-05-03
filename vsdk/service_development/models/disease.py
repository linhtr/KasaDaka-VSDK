from django.db import models
from django.conf import settings

from .voicelabel import VoiceLabel

class Disease(models.Model):
    name = models.CharField(max_length=200)
    voice_label = models.ForeignKey(
            VoiceLabel,
            verbose_name = 'Voice label',
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )

    def __str__(self):
        return self.name

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