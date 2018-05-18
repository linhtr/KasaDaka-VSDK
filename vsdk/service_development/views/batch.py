from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

from ..models import KasaDakaUser, CallSession, Language, Disease, VoiceLabel

from . import base

class BatchSubmission(TemplateView):

    def render_batch_submission_form(self, request, session, redirect_url):
        diseases = Disease.objects.all()

        # This is the redirect URL to POST the disease submission
        redirect_url_POST = reverse('service-development:batch-submit', args = [session.id])

        # This is the redirect URL for *AFTER* the disease submission process
        pass_on_variables = {'redirect_url' : redirect_url}

        language = session.language
        ask_submit_batch_voice_label = language.get_interface_voice_label_url_dict["ask_submit_batch"]
        batch_days_ago_voice_label = language.get_interface_voice_label_url_dict["batch_days_ago"]

        context = { 'session' : session,
                    'ask_submit_batch_voice_label' : ask_submit_batch_voice_label,
                    'batch_days_ago_voice_label' : batch_days_ago_voice_label,
                    'redirect_url_POST' : redirect_url_POST,
                    'pass_on_variables' : pass_on_variables
                   }
        return render(request, 'batch_submit.xml', context, content_type='text/xml')

    def get(self, request, session_id):
        """
        Asks the user to do a disease submission
        """
        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = session.service
        if 'redirect_url' in request.GET:
            redirect_url = request.GET['redirect_url']
        else:
            redirect_url = None
        return self.render_batch_submission_form(request, session, redirect_url)

    def post(self, request, session_id):
        """
        Saves the disease submissions
        """
        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else:
            raise ValueError('Incorrect request, redirect_url not set')

        if 'days_ago' not in request.POST:
            days_ago = 0

        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = session.service

        user = get_object_or_404(Disease, pk = session.user_id)

        batch = Batch()
        batch.user = user
        batch.date = datetime.now() - timedelta(days = days_ago)
        batch.save()

        if not batch.id:
            raise ObjectDoesNotExist

        batch.schedule_vaccinations()

        return HttpResponseRedirect(redirect_url)
