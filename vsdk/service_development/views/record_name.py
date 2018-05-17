from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *


# def record_get_redirect_url(record_element, session):
#     return record_element.redirect.get_absolute_url(session)

def record_generate_context(session, redirect_url):
    language = session.language
    # redirect_url = record_get_redirect_url(record_element, session)


    # voice_label = record_element.voice_label.get_voice_fragment_url(language)
    # ask_confirmation_voice_label = record_element.ask_confirmation_voice_label.get_voice_fragment_url(language)
    # repeat_voice_label = record_element.repeat_voice_label.get_voice_fragment_url(language)
    # final_voice_label = record_element.final_voice_label.get_voice_fragment_url(language)
    # did_not_hear_voice_label = record_element.not_heard_voice_label.get_voice_fragment_url(language)

    ask_name = language.get_interface_voice_label_url_dict["ask_name"]
    ask_confirmation_voice_label = language.get_interface_voice_label_url_dict["ask_confirmation"]
    repeat_voice_label = language.get_interface_voice_label_url_dict["repeat"]
    final_voice_label = language.get_interface_voice_label_url_dict["final"]
    did_not_hear_voice_label = language.get_interface_voice_label_url_dict["did_not_hear"]
    repeat_recording_to_caller = True
    ask_confirmation = True
    max_time_input = 180
    barge_in = True

    context = {
               'redirect_url': redirect_url,
               'voice_label' : ask_name,
               'ask_confirmation_voice_label' : ask_confirmation_voice_label,
               'repeat_voice_label' : repeat_voice_label ,
               'final_voice_label' : final_voice_label,
               'did_not_hear_voice_label' : did_not_hear_voice_label,
               'max_time_input' : max_time_input,
               'repeat_recording_to_caller' : repeat_recording_to_caller,
               'ask_confirmation' : ask_confirmation,
               'barge_in' : barge_in
               }

    return context


def record_name(request, user_id, session_id):

    user = get_object_or_404(KasaDakaUser, pk=user_id)
    voice_service = user.service
    session = lookup_or_create_session(voice_service, session_id)

    if 'redirect_url' in request.GET:
        redirect_url = request.GET['redirect_url']
    elif 'redirect_url' in request.POST:
        redirect_url = request.POST['redirect_url']
    else:
        redirect_url = reverse('service-development:user-registration', args =[session.id])

    if request.method == "POST":
        session = get_object_or_404(CallSession, pk=session_id)

        value = 'audio file'

        result = SpokenUserInput()

        result.session = session

        result.audio = request.FILES['recording']
        result.audio.name = 'name_recording_s%s_u%s.wav' % (session_id, user_id)
        result.category = record_element.input_category

        result.save()

        user.name_voice = result
        user.save ()

        #if record_element.map_to_call_session_property in vars(session).keys():
        #    setattr(session, record_element.map_to_call_session_property, value)

        # redirect to next element
        return redirect(request.POST['redirect'])


    # session.record_step(record_element)

    context = record_generate_context(session, redirect_url)

    context['url'] = request.get_full_path(False)

    return render(request, 'record_name.xml', context, content_type='text/xml')
