from django.http import HttpResponse, Http404
from django.contrib.auth.hashers import make_password
import random


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