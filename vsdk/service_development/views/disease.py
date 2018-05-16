from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import KasaDakaUser, CallSession, Language, Disease, VoiceLabel

from . import base

class DiseaseSubmission(TemplateView):

    def render_disease_selection_form(self, request, session, redirect_url):
        diseases = Disease.objects.all()

        # This is the redirect URL to POST the disease submission
        redirect_url_POST = reverse('service-development:disease-submission', args = [session.id])

        # This is the redirect URL for *AFTER* the disease submission process
        pass_on_variables = {'redirect_url' : redirect_url}

        diseases_voice_labels = [disease.get_voice_fragment_url(session.language) for disease in Disease.objects.all()]
        # for disease in diseases:
        #     print(disease)
        #     diseases_voice_labels.append(disease.get_voice_fragment_url(session.language))

        context = { 'session' : session,
                    'diseases' : diseases,
                    'diseases_voice_labels' : diseases_voice_labels,
                    'redirect_url' : redirect_url_POST,
                    'amount_voice_label' : VoiceLabel.objects.get(pk=59), # TODO REMOVE THIS HARDCODED NONCENSE
                    'pass_on_variables' : pass_on_variables
                   }
        return render(request, 'disease_submission.xml', context, content_type='text/xml')

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
        return self.render_disease_selection_form(request, session, redirect_url)

    def post(self, request, session_id):
        """
        Saves the disease submissions
        """
        if 'redirect_url' in request.POST:
            redirect_url = request.POST['redirect_url']
        else:
            raise ValueError('Incorrect request, redirect_url not set')

        if 'disease_id' not in request.POST:
            raise ValueError('Incorrect request, disease ID not set')

        if 'disease_amount' not in request.POST:
            raise ValueError('Incorrect request, amount diseased not set')

        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = session.service

        user = get_object_or_404(Disease, pk = session.user_id)
        disease = get_object_or_404(KasaDakaUser, pk = request.POST['disease_id'])

        user_disease, created = UsersDiseases.objects.get_or_create(user=user, disease=disease)
        user_disease.amount = request.POST['disease_amount']
        user_disease.save()

        return HttpResponseRedirect(redirect_url)
