from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django import http
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from bio import models as bio_api
from bio.utils import create_s3_policy_doc
from bio.emails import send_user_link

import hmac, hashlib
import random


def check_user(method):
    def call_view(*args, **kwargs):
        request = args[0]
        key = request.GET.get('key', None)
        if not key:
            return method(*args, **kwargs)
        try:
            bio = bio_api.get_bio_by_secret(key)
        except:
            return method(*args, **kwargs)
        request.session['user_email'] = bio['email']
        if request.session.get('user_bio'):
            del request.session['user_bio']
        # TODO - do we still need to do this?
        try:
            request.session['user_bio'] = bio
        except:
            pass
        return http.HttpResponseRedirect(request.path)
    return call_view


@check_user
def sequence_redirect(request):
    # TODO if we have a signed in user, we should redirect to the right sequence
    current_sequence = None #sequence_api.get_current_sequence_number()
    if not current_sequence:
        return http.HttpResponseNotFound()
    url = reverse('bio_bio', kwargs={'sequence':current_sequence})
    return http.HttpResponseRedirect(url)


@check_user
def bio(request, sequence):
    """ show bio for all signups for this sequence with profiles """
    s3_policy, signature = create_s3_policy_doc(settings.AWS_S3_BUCKET, 'bio')

    prefix = hmac.new(
        'THEANSWERIS42', request.session.session_key, hashlib.sha1
    ).hexdigest()

    bios = bio_api.get_bios(sequence, limit=0)
    bios += [{'email': ''} for i in range(len(bios), 36)]
    bios = random.sample(bios, 36)

    # if user is logged in and has a bio, display it!
    user_bio = request.session.get('user_bio', None)
    if user_bio:
        bio_in_list = [ x for x in bios if x['email'] == user_bio['email'] ]
        if len(bio_in_list) == 1:
            # swap user bio with bio at position 12
            bio_index = bios.index(bio_in_list[0])
            bios[bio_index] = bios[11]
        bios[11] = user_bio
    else:
        # make a gap at position 12
        bios[11] = {'email': ''}

    context = {
        'bios': bios,
        'user_bio': user_bio,
        'user_email': request.session.get('user_email'),
        'sequence': sequence,
        's3_policy': s3_policy,
        's3_signature': signature,
        'AWS_ACCESS_KEY_ID': settings.AWS_ACCESS_KEY_ID,
        'AWS_S3_BUCKET': settings.AWS_S3_BUCKET,
        'key_prefix': 'bio/{0}'.format(prefix)
    }
    
    return render_to_response('bio/index.html', context, context_instance=RequestContext(request))


@require_http_methods(['POST'])
def save_bio(request, sequence):
    """ receive AJAX post from class bio page """

    url = reverse('bio_bio', kwargs={'sequence': sequence})

    # TODO validate data on the server side also!

    if request.POST['email'] != request.session.get('user_email'):
        messages.error(request, 'Oops! We don\'t recognize that email. Maybe you signed up with a different one?')
        return http.HttpResponseRedirect(url)

    user_bio = bio_api.save_bio(
        request.POST['email'],
        sequence,
        request.POST['name'],
        request.POST['bio'],
        request.POST['avatar'],
        request.POST.get('twitter', None),
        request.POST.get('gplus', None)
    )
    request.session['user_bio'] = user_bio
    
    messages.success(request, 'Sweet! You\'re now in the Class Photo!')

    return http.HttpResponseRedirect(url)


@require_http_methods(['POST'])
def request_link(request, sequence):
    bio = None
    if bio_api.has_bio( request.POST.get('email'), sequence):
        bio = bio_api.get_bio( request.POST.get('email'), sequence)
    else:
        bio = bio_api.save_bio( request.POST.get('email'), sequence, '', '', '')
    messages.success(request, 'Check your inbox -- a tasty new link will be there shortly.')
    #TODO send_user_link(bio['email'], sequence, bio['secret'])
    url = reverse('bio_bio', kwargs={'sequence': sequence})
    if settings.DEBUG:
        url += '?key={0}'.format(bio['secret'])
    return http.HttpResponseRedirect(url)


def clear_session(request):
    if request.session.get('user_bio'):
        del request.session['user_bio']
    if request.session.get('user_email'):
        del request.session['user_email']
    return http.HttpResponseRedirect(reverse('bio_sequence_redirect'))
