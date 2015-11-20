# -*- coding: utf-8 -*-

import django
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Departments, ListHistory, ListDiary, ListAnalysis, LaboratoryData
from models import ActiveDepart, ListExamens, History, PatientInfo
from models import TemperatureList, NurseViewList, PainStatusList, RiskDownList
from models import TemperatureData, RiskDownData, PainStatus
from models import ListSurgery, SurgeryAdv
from django.db.models import Q
from django.utils.safestring import mark_safe


def index(request):
    """
    Главная страница
    :param request:
    :return:
    """
    current_doctor = 'Бекмуратов Ж.А.'

    return render_to_response('index.html',
        {
            'current_doc': current_doctor,
            'title': 'Главная страница',
        },
        context_instance=RequestContext(request))


def search(request):
    """
    Результаты поиска по номеру истории, ФИО пациента
    :param request:
    :return: Список найденных историй болезни
    """
    if request.method == "POST":
        find_string = request.POST['patient']
        patients = ListHistory.objects.filter(Q(num_history__startswith=find_string) | Q(lastname__iexact=find_string)).order_by('receipt')
        where_find = mark_safe(u"Результаты поиска по <em>" + find_string + "</em>")
        return render_to_response('patients.html',
                                  {
                                      'patients': patients,
                                      'title': 'Поиск',
                                      'current_place': where_find,
                                  })


def login(request):
    return RequestContext('login.html')

def get_my_patient(request):
    """
    Мои пациенты
    :param request:
    :return: Список найденных историй по выбранному врачу
    """
    iddoctor = 5010
    current_doc = 'Бекмуратов Ж.А.'
    patients = ListHistory.objects.filter(id_doctor=iddoctor).filter(discharge__isnull=True)
    return render_to_response('patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
            'title': 'Мои пациенты',
            'current_place': u'Мои пациенты',
        })


def get_patient_info(request, idpatient):
    patient = History.objects.get(pk=idpatient)
    return render_to_response('patient_info.html',
                       {
                           'patient': patient,
                       })


def get_patient_first_view(request, idpatient):
    patient = History.objects.get(pk=idpatient)
    first_view = PatientInfo.objects.filter(id_history=idpatient).filter(id_view=0)
    return render_to_response('patient_firstview.html',
                       {
                           'patient': patient,
                           'first_view': first_view,
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

    diarys = ListDiary.objects.filter(id_history=idpatient).order_by('-reg_date')
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
    depart = Departments.objects.get(pk=iddepart)
    return render_to_response('patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
            'current_place': depart.name,
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


def get_list_surgery(request, idpatient):
    history = ListHistory.objects.filter(id=idpatient)
    patient = history[0].lastname
    numhistory = history[0].num_history
    surgery = ListSurgery.objects.filter(id_history=idpatient).order_by('surgery_date')
    return render_to_response('list_surgery.html',
                              {
                                  'surgery': surgery,
                                  'idpatient': idpatient,
                                  'num': numhistory,
                                  'patient': patient,
                              })


def get_operation(request, id):
    operation = ListSurgery.objects.get(pk=id)
    adv_info = ''
    if (operation.type_operation == 1):
        advanced = SurgeryAdv.objects.filter(id_surgery=id).filter(id_type=9)
        adv_info = advanced[0].text_value
    return render_to_response('operation.html',
                              {
                                  'operation': operation,
                                  'adv_info': adv_info,
                              })