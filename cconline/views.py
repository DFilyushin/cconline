# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
import django
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Departments, ListHistory, ListDiary, ListAnalysis, LaboratoryData
from models import ActiveDepart, ListExamens, History
from models import TemperatureList, NurseViewList, PainStatusList, RiskDownList
from models import TemperatureData, RiskDownData, PainStatus


def index(request):
    departs = Departments.objects.all().order_by('name')
    current_doctor = 'Ельмеева Т.Н.'

    return render_to_response('index.html',
        {
            'current_doc': current_doctor,
            'title': 'Главная страница',
        },
        context_instance=RequestContext(request))


def get_my_patient(request):
    iddoctor = 5010
    current_doc = 'Ельмеева Т.Н.'
    patients = ListHistory.objects.filter(id_doctor=iddoctor).filter(discharge__isnull=True)
    return render_to_response('patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
            'title': 'Мои пациенты',
        })


def get_patient_info(request, id):
    patient = History.objects.get(pk=id)
    render_to_response('patient_info.html',
                       {
                           'patient': patient,
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

def get_active_departs(request):
    departs = ActiveDepart.objects.all()
    return render_to_response('departs.html',
                              {
                                  'departs': departs,
                              })


def patients_by_depart(request, iddepart):
    iddoctor = 5010
    current_doc = 'Ельмеева Т.Н.'
    patients = ListHistory.objects.filter(id_depart=iddepart).filter(discharge__isnull=True)
    return render_to_response('patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
        })


def get_examen_list(request, idpatient):
    examens = ListExamens.objects.filter(id_history=idpatient).order_by('-date_plan')
    history = ListHistory.objects.filter(id=idpatient)
    patient = history[0].lastname
    numhistory = history[0].num_history
    return render_to_response('list_examens.html',
                              {
                                  'examens': examens,
                                  'patient': patient,
                                  'num': numhistory,
                                  'idpatient': idpatient,
                              })

def get_examen(request, id):
    examen = ListExamens.objects.get(pk=id)
    return render_to_response('examen.html',
                              {
                                  'examen': examen,
                              })


def get_nurse_list(request, idpatient):
    history = ListHistory.objects.filter(id=idpatient)
    patient = history[0].lastname
    numhistory = history[0].num_history
    temp_list = TemperatureList.objects.filter(id_history=idpatient)
    view_list = NurseViewList.objects.filter(id_history=idpatient)
    pain_list = PainStatusList.objects.filter(id_history=idpatient)
    down_list = RiskDownList.objects.filter(id_history=idpatient)
    return render_to_response('nurse.html',
                              {
                                  'temp_list': temp_list,
                                  'view_list': view_list,
                                  'pain_list': pain_list,
                                  'down_list': down_list,
                                  'patient': patient,
                                  'num': numhistory,
                                  'idpatient': idpatient,
                              })


def get_tempearature_data(request, id):
    view = TemperatureList.objects.get(pk=id)
    values = TemperatureData.objects.filter(id_ctrl_nurse=id)
    return render_to_response('temp_list.html',
                       {
                           'view': view,
                           'values': values,
                       })


def get_risk_down(request, id):
    view = RiskDownData.objects.get(pk=id)
    return render_to_response('risk_down.html',
                              {
                                  'view': view,
                              })


def get_pain_status(request, id):
    view = PainStatus.objects.get(pk=id)
    return render_to_response('pain_status.html',
                              {
                                  'view': view,
                              })