# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
import random
from django.template.loader import get_template
from django.template import Context


def getpass(request):
    # create pass sha256 for client ;-)
    user_pass = request.GET.get('pass')
    salt = request.GET.get('salt', '-')
    if not user_pass:
        raise Http404
    if salt == '-':
        salt = str(random.randint(1000, 9000))
    password = make_password(user_pass, salt, 'pbkdf2_sha256')
    return HttpResponse(password, mimetype='text/html')


def gethttp(request):
    # для внешних адресов нельзя вызывать запрос
    remote_address = request.META['REMOTE_ADDR']
    is_local_net = ('192.168.100' in remote_address) or ('127.0.0.1' in remote_address)
    if not is_local_net:
        raise Http404
    template = get_template('cconline/test.html')
    page_data = { 'REQ_META': request.META, 'is_local_net': is_local_net, }
    context = template.render(Context(page_data))
    return HttpResponse(context)


def page_not_found(request):
    response = render_to_response('404.html',
                                  {},
                                  context_instance = RequestContext(request)
                                  )
    response.status_code = 404
    return response
