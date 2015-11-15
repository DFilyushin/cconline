# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
import django
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Departments, ListHistory, ListDiary, ListAnalysis, LaboratoryData


def index(request):
    departs = Departments.objects.all().order_by('name')
    current_doctor = 'Ельмеева Т.Н.'

    return render_to_response('index.html',
        {
            'current_doc': current_doctor,
        },
        context_instance=RequestContext(request))


def get_my_patient(request):
    iddoctor = 5038
    current_doc = 'Ельмеева Т.Н.'
    patients = ListHistory.objects.filter(id_doctor=iddoctor).filter(discharge__isnull=True)
    return render_to_response('patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
        })

def get_patient(request, idpatient):
    patient = ListHistory.objects.filter(id=idpatient)[0].lastname
    numhistory = ListHistory.objects.filter(id=idpatient)[0].num_history
    return render_to_response('patient.html',
        {
            'patient': patient,
            'id': idpatient,
            'num': numhistory,
        })

def get_diary_list(request, idpatient):
    diarys = ListDiary.objects.filter(id_history=idpatient)
    history = ListHistory.objects.filter(id=idpatient)
    patient = history[0].lastname
    numhistory = history[0].num_history
    return render_to_response('list_diary.html',
                              {
                                  'diarys': diarys,
                                  'patient': patient,
                                  'num': numhistory,
                                  'idpatient': idpatient,
                              })

def get_diary(request, id):
    diary = ListDiary.objects.get(pk=id)
    idpatient = diary.id_history
    history = ListHistory.objects.filter(id=idpatient)
    patient = history[0].lastname
    numhistory = history[0].num_history
    return render_to_response('diary.html',
                              {
                                  'diary': diary,
                                  'patient':patient,
                                  'num': numhistory,
                              })


def get_lab_list(request, idpatient):
    labs = ListAnalysis.objects.filter(id_history=idpatient)
    history = ListHistory.objects.filter(id=idpatient)
    patient = history[0].lastname
    numhistory = history[0].num_history
    return render_to_response('list_laboratory.html',
                              {
                                  'labs': labs,
                                  'patient': patient,
                                  'num': numhistory,
                                  'idpatient': idpatient,
                              })

def get_laboratory(request, id):
    lab = ListAnalysis.objects.get(pk=id)
    lab_result = LaboratoryData.objects.filter(id_assigned_anal=id).order_by('sort_pos')
    return render_to_response('laboratory.html',
                              {
                                  'order': lab,
                                  'result': lab_result,
                              })