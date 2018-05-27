from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def record_generate_context(session, redirect_url):
    language = session.language


    ask_name_voice_label = language.get_interface_voice_label_url_dict["ask_name"]
    ask_confirmation_voice_label = language.get_interface_voice_label_url_dict["ask_confirmation"]
    repeat_voice_label = language.get_interface_voice_label_url_dict["repeat"]
    final_voice_label = language.get_interface_voice_label_url_dict["final"]
    did_not_hear_voice_label = language.get_interface_voice_label_url_dict["did_not_hear"]
    repeat_recording_to_caller = True
    ask_confirmation = True
    max_time_input = 180
    barge_in = False
    redirect_url_post = reverse('service-development:record_name', args =[session.user.id, session.id])

    context = {
               'redirect_url': redirect_url,
               'ask_name_voice_label' : ask_name_voice_label,
               'ask_confirmation_voice_label' : ask_confirmation_voice_label,
               'repeat_voice_label' : repeat_voice_label ,
               'final_voice_label' : final_voice_label,
               'did_not_hear_voice_label' : did_not_hear_voice_label,
               'max_time_input' : max_time_input,
               'repeat_recording_to_caller' : repeat_recording_to_caller,
               'ask_confirmation' : ask_confirmation,
               'barge_in' : barge_in,
               "end_call_voice_label" : language.get_interface_voice_label_url_dict["end_call"],
               "redirect_url_post" : redirect_url_post
               }

    return context


def record_name(request, user_id, session_id):

    user = get_object_or_404(KasaDakaUser, pk=user_id)
    voice_service = user.service
    session = lookup_or_create_session(voice_service, session_id)
    print("recordtest1")
    if 'redirect_url' in request.GET:
        redirect_url = request.GET['redirect_url']
    elif 'redirect_url' in request.POST:
        redirect_url = request.POST['redirect_url']
    else:
        redirect_url = reverse('service-development:user-registration', args =[session.id])

    print("recordtest2")
    if request.method == "POST":
        print("recordtest31")
        session = get_object_or_404(CallSession, pk=session_id)

        value = 'audio file'

        print("recordtest32")
        result = SpokenUserInput()

        print("recordtest33")
        result.session = session
        print("recordtest34")

        result.audio = request.FILES['recording']
        result.audio.name = 'name_recording_s%s_u%s.wav' % (session_id, user_id)
        result.category = UserInputCategory.get(name="username")

        result.save()
        print("recordtest35")

        user.name_voice = result
        user.save ()
        print("recordtest36")

        # redirect to next element
        return redirect(redirect_url)

    context = record_generate_context(session, redirect_url)
    print("recordtest41")
    context['url'] = request.get_full_path(False)
    print("recordtest42")

    print(request)
    print(context)

    return render(request, 'record_name.xml', context, content_type='text/xml')
