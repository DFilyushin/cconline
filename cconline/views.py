# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
import django
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Departments, ListHistory


def index(request):
    departs = Departments.objects.all().order_by('name')
    current_doctor = 'Ельмеева Т.Н.'

    return render_to_response('index.html',
        {
            'current_doc': current_doctor,
        },
        context_instance=RequestContext(request))


def get_my_patient(request):
    iddoctor = 1084
    current_doc = 'Ельмеева Т.Н.'
    patients = ListHistory.objects.filter(id_doctor=iddoctor).filter(discharge__isnull=True)
    return render_to_response('patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
        })