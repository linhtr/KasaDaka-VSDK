from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from vsdk.service_development.models import VoiceLabel
from .vs_element import VoiceServiceElement
from .user_input import UserInputCategory

class Digits(VoiceServiceElement):
    _urls_name = 'service-development:digits'

    no_digits_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('No digits voice label'),
        help_text = _('The voice label that is played when the system does not received any digits from the user. Example: "We did receive any number, please enter the number on the keyboard."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='no_digits_voice_label'
    )
    barge_in = models.BooleanField(_('Allow the caller to start typing immediately'), default=True)
    repeat_digits_to_caller = models.BooleanField(_('Repeat the digits to the caller before asking for confirmation'), default=True)
    repeat_digits_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Repeat digits voice label'),
        help_text = _('The voice label that is played before the system repeats the user digit input. Example: "You entered:"'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='repeat_digits_voice_label'
    )
    ask_confirmation_digits = models.BooleanField(
        _('Ask the caller to confirm their digit input'), default=True)
    ask_confirmation_digits_voice_label = models.ForeignKey(
        VoiceLabel,
        verbose_name = _('Ask for confirmation voice label'),
        help_text = _('The voice label that asks the user to confirm their pinput. Example: "Is this correct? Press 1 to confirm, or press 2 to retry."'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmation_digits_voice_label',
    )

    _redirect = models.ForeignKey(
            VoiceServiceElement, 
            on_delete = models.SET_NULL,
            verbose_name = _('Redirect element'),
            help_text = _("The element to redirect after user' confirmation of key input."),
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)
    
    class Meta:
        verbose_name = _('Digit Input Element')

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect:
            return VoiceServiceElement.objects.get_subclass(id=self._redirect.id)
        else:
            return None

    def __str__(self):
        return "Digits: " + self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(Record, self).validator())
        if not self._redirect:
            errors.append(ugettext('Digits %s does not have a redirect element') % self.name)
        return errors