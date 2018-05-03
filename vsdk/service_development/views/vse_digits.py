from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


def digits_get_redirect_url(digits_element, session):
    return digits_element.redirect.get_absolute_url(session)

def digits_generate_context(digits_element, session):
    language = session.language
    redirect_url = digits_get_redirect_url(digits_element, session)


    digits_voice_label = digits_element.digits_voice_label.get_voice_fragment_url(language)
    ask_confirmation_digits_voice_label = digits_element.ask_confirmation_digits_voice_label.get_voice_fragment_url(language)
    repeat_digits_voice_label = digits_element.repeat_digits_voice_label.get_voice_fragment_url(language)
    no_digits_voice_label = record_element.no_digits_voice_label.get_voice_fragment_url(language)

    context = {'digits': digits_element,
               'redirect_url': redirect_url,
               'digits_voice_label' : digits_voice_label,
               'ask_confirmation_digits_voice_label' : ask_confirmation_digits_voice_label,
               'repeat_digits_voice_label' : repeat_digits_voice_label,
               'no_digits_voice_label' : no_digits_voice_label,
               }

    return context


def digits(request, element_id, session_id):
    digits_element = get_object_or_404(Digits, pk=element_id)
    voice_service = digits_element.service
    session = lookup_or_create_session(voice_service, session_id)


    if request.method == "POST":
        session = get_object_or_404(CallSession, pk=session_id)

        value = 'digit input'

        result = UserDigitInput()

        result.session = session

        result.category = digits_element.input_category 

        result.save()

        # redirect to next element
        return redirect(request.POST['redirect'])


    session.digits_step(digits_element)
    context = digits_generate_context(digits_element, session)

    context['url'] = request.get_full_path(False)

    return render(request, 'digits.xml', context, content_type='text/xml')