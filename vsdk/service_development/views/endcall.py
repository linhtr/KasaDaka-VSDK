from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

from ..models import KasaDakaUser, CallSession, Language, Disease, VoiceLabel, Batch

from . import base

class EndCall(TemplateView):

    def get(self, request, session_id):
        """
        Ends the call
        """
        session = get_object_or_404(CallSession, pk = session_id)
        language = session.language
        if language == None:
            language = Language.objects.get(code="en")
        print()
        print()
        print(session)
        print()
        print()
        context = { "end_call_voice_label" : language.get_interface_voice_label_url_dict["end_call"] }
        return render(request, 'end_call.xml', context, content_type='text/xml')
