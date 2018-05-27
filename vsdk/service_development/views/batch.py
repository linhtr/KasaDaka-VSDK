from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

from ..models import KasaDakaUser, CallSession, Language, Disease, VoiceLabel, Batch

from . import base

class BatchSubmission(TemplateView):

    def render_batch_submission_form(self, request, session, redirect_url):
        diseases = Disease.objects.all()

        # This is the redirect URL to POST the batch submission
        redirect_url_POST = reverse('service-development:batch-submit', args = [session.id])

        # This is the redirect URL for *AFTER* the batch submission process
        pass_on_variables = {'redirect_url' : redirect_url}

        language = session.language
        welcome_user_voice_label = language.get_interface_voice_label_url_dict["welcome_user"]
        ask_submit_batch_voice_label = language.get_interface_voice_label_url_dict["ask_submit_batch"]
        batch_days_ago_voice_label = language.get_interface_voice_label_url_dict["batch_days_ago"]
        thank_you_submitted_voice_label = language.get_interface_voice_label_url_dict["thank_you_submitted"]
        end_call_voice_label = language.get_interface_voice_label_url_dict["end_call"]

        context = { 'session' : session,
                    'welcome_user_voice_label' : welcome_user_voice_label,
                    'ask_submit_batch_voice_label' : ask_submit_batch_voice_label,
                    'batch_days_ago_voice_label' : batch_days_ago_voice_label,
                    'thank_you_submitted_voice_label' : thank_you_submitted_voice_label,
                    'end_call_voice_label' : end_call_voice_label,
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
        print("batchtest1")
        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else:
            raise ValueError('Incorrect request, redirect_url not set')
        print("batchtest2")
        if 'days_ago' in request.POST:
            days_ago = int(request.POST['days_ago'])
        else:
            days_ago = 0

        session = get_object_or_404(CallSession, pk = session_id)
        print("batchtest3")
        voice_service = session.service
        print("batchtest4")
        user = get_object_or_404(KasaDakaUser, pk = session.user_id)
        print("batchtest5")
        batch = Batch()
        print("batchtest6")
        batch.user = user
        print("batchtest7")
        batch.date = datetime.now() - timedelta(days = days_ago)
        print("batchtest8")
        batch.save()
        print("batchtest9")

        if not batch.id:
            raise ObjectDoesNotExist
        print("batchtest10")

        batch.schedule_vaccinations()
        print("batchtest11")

        return HttpResponseRedirect(redirect_url)
