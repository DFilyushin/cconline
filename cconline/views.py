# -*- coding: utf-8 -*-

import django
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Departments, ListHistory, ListDiary, ListAnalysis, LaboratoryData
from models import ActiveDepart, ListExamens, History, PatientInfo, HistoryMedication
from models import TemperatureList, NurseViewList, PainStatusList, RiskDownList
from models import TemperatureData, RiskDownData, PainStatus
from models import ListSurgery, SurgeryAdv, ListProffView, Medication
from models import SysUsers, UserGroups
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout


def card_login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(604800)
    return login(request, *args, **kwargs)


def get_current_doctor(request):
    current_user = request.user.username.upper()
    card_user = SysUsers.objects.get(pk=current_user)
    return card_user.user_fullname


def get_user_groups(request):
    current_user = request.user.username.upper()
    list_group = UserGroups.objects.filter(sys_login=current_user)
    return [item.sys_group for item in list_group]


@login_required(login_url='/login')
def index(request):
    """
    Главная страница
    :param request:
    :return:
    """
    return render_to_response('cconline/index.html',
        {
            'current_doc': get_current_doctor(request),
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
        return render_to_response('cconline/patients.html',
                                  {
                                      'patients': patients,
                                      'title': 'Поиск',
                                      'current_place': where_find,
                                      'current_doc': get_current_doctor(request),
                                  })


@login_required(login_url='/login')
def get_my_patient(request):
    """
    Мои пациенты
    :param request:
    :return: Список найденных историй по выбранному врачу
    """
    current_user = request.user.username.upper()
    card_user = SysUsers.objects.get(pk=current_user)
    iddoctor = card_user.id_doctor
    current_doc = card_user.user_fullname
    patients = ListHistory.objects.filter(id_doctor=iddoctor).filter(discharge__isnull=True)
    return render_to_response('cconline/patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
            'title': 'Мои пациенты',
            'current_place': u'Мои пациенты',
        })


def get_patient_info(request, idpatient):
    patient = History.objects.get(pk=idpatient)
    return render_to_response('cconline/patient_info.html',
                       {
                           'patient': patient,
                       })


def get_patient_first_view(request, idpatient):
    patient = History.objects.get(pk=idpatient)
    first_view = PatientInfo.objects.filter(id_history=idpatient).filter(id_view=0)
    return render_to_response('cconline/patient_firstview.html',
                       {
                           'patient': patient,
                           'first_view': first_view,
                       })


def get_patient(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404

    return render_to_response('cconline/patient.html',
        {
            'patient': history.lastname,
            'id': idpatient,
            'num': history.num_history,
            'current_doc': get_current_doctor(request),
            'list_group': get_user_groups(request),
        })


def get_diary_list(request, idpatient):
    """
    Список дневников пациента
    :param request:
    :param idpatient: Код пациента
    :return: Список дневников
    """
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    diarys = ListDiary.objects.filter(id_history=idpatient).order_by('-reg_date')
    return render_to_response('cconline/list_diary.html',
                              {
                                  'diarys': diarys,
                                  'history': history,
                              })


def get_diary(request, id):
    try:
        diary = ListDiary.objects.get(pk=id)
    except ListDiary.DoesNotExist:
        raise Http404
    history = ListHistory.objects.get(pk=diary.id_history)
    return render_to_response('cconline/diary.html',
                              {
                                  'diary': diary,
                                  'history': history,
                              })


def get_lab_list(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    labs = ListAnalysis.objects.filter(id_history=idpatient)
    return render_to_response('cconline/list_laboratory.html',
                              {
                                  'labs': labs,
                                  'history': history,
                              })


def get_laboratory(request, id):
    """
    Данные одного лабораторного анализа
    :param request:
    :param id: Код анализа (pk)
    :return:
    """
    try:
        lab = ListAnalysis.objects.get(pk=id)
    except ListAnalysis.DoesNotExist:
        raise Http404
    lab_result = LaboratoryData.objects.filter(id_assigned_anal=id).order_by('sort_pos')
    return render_to_response('cconline/laboratory.html',
                              {
                                  'order': lab,
                                  'result': lab_result,
                              })


def get_active_departs(request):
    departs = ActiveDepart.objects.all()
    return render_to_response('cconline/departs.html',
                              {
                                  'departs': departs,
                              })


def patients_by_depart(request, iddepart):
    """
    Список пациентов по отделениям
    :param request:
    :param iddepart:
    :return:
    """
    try:
        depart = Departments.objects.get(pk=iddepart)
    except Departments.DoesNotExist:
        raise Http404

    patients = ListHistory.objects.filter(id_depart=iddepart).filter(discharge__isnull=True)
    return render_to_response('cconline/patients.html',
        {
            'patients': patients,
            'current_place': depart.name,
            'current_doc': get_current_doctor(request),
        })


def get_examen_list(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    examens = ListExamens.objects.filter(id_history=idpatient).order_by('-date_plan')
    patient = history.lastname
    numhistory = history.num_history
    return render_to_response('cconline/list_examens.html',
                              {
                                  'examens': examens,
                                  'patient': patient,
                                  'num': numhistory,
                                  'idpatient': idpatient,
                              })


def get_examen(request, id):
    """
    Данные обследования
    :param request:
    :param id: Код обследования (pk)
    :return:
    """
    try:
        examen = ListExamens.objects.get(pk=id)
    except ListExamens.DoesNotExist:
        raise Http404
    return render_to_response('cconline/examen.html',
                              {
                                  'examen': examen,
                              })


def get_nurse_list(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    patient = history.lastname
    numhistory = history.num_history
    temp_list = TemperatureList.objects.filter(id_history=idpatient)
    view_list = NurseViewList.objects.filter(id_history=idpatient)
    pain_list = PainStatusList.objects.filter(id_history=idpatient)
    down_list = RiskDownList.objects.filter(id_history=idpatient)
    return render_to_response('cconline/nurse.html',
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
    try:
        view = TemperatureList.objects.get(pk=id)
    except TemperatureList.DoesNotExist:
        raise Http404

    values = TemperatureData.objects.filter(id_ctrl_nurse=id)
    return render_to_response('cconline/temp_list.html',
                       {
                           'view': view,
                           'values': values,
                       })


def get_risk_down(request, id):
    try:
        view = RiskDownData.objects.get(pk=id)
    except RiskDownData.DoesNotExist:
        raise Http404

    return render_to_response('cconline/risk_down.html',
                              {
                                  'view': view,
                              })


def get_pain_status(request, id):
    try:
        view = PainStatus.objects.get(pk=id)
    except PainStatus.DoesNotExist:
        raise Http404

    return render_to_response('cconline/pain_status.html',
                              {
                                  'view': view,
                              })


def get_list_surgery(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    patient = history.lastname
    numhistory = history.num_history
    surgery = ListSurgery.objects.filter(id_history=idpatient).order_by('surgery_date')
    return render_to_response('cconline/list_surgery.html',
                              {
                                  'surgery': surgery,
                                  'idpatient': idpatient,
                                  'num': numhistory,
                                  'patient': patient,
                              })


def get_list_proffview(request, idpatient):
    """
    Список осмотров профильными специалистами
    :param request:
    :param idpatient:
    :return:
    """
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404

    patient = history.lastname
    numhistory = history.num_history
    dataset = ListProffView.objects.filter(id_history=idpatient)
    return render_to_response('cconline/list_prof_view.html',
                              {
                                  'proflist': dataset,
                                  'idpatient': idpatient,
                                  'num': numhistory,
                                  'patient': patient,
                              })


def get_proview(request, id):
    """

    :param request:
    :param id:
    :return:
    """
    try:
        proview = ListProffView.objects.get(pk=id)
    except ListProffView.DoesNotExist:
        raise Http404

    pages = PatientInfo.objects.filter(id_history=proview.id_history).filter(id_view=id)
    return render_to_response('cconline/proview.html',
                              {
                                  'proview': proview,
                                  'pages': pages,
                                  'idpatient': proview.id_history,
                                  'num': proview.num_history,
                                  'patient': proview.patient,
                              })


def get_operation(request, id):
    try:
        operation = ListSurgery.objects.get(pk=id)
    except ListSurgery.DoesNotExist:
        raise Http404
    adv_info = ''
    if (operation.type_operation == 1):
        advanced = SurgeryAdv.objects.filter(id_surgery=id).filter(id_type=9)
        adv_info = advanced[0].text_value
    return render_to_response('cconline/operation.html',
                              {
                                  'operation': operation,
                                  'adv_info': adv_info,
                              })


def get_list_medication(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    patient = history.lastname
    numhistory = history.num_history
    dataset = HistoryMedication.objects.filter(id_history=idpatient)
    return render_to_response('cconline/list_medication.html',
                              {
                                  'dataset': dataset,
                                  'num': numhistory,
                                  'patient': patient,
                                  'idpatient': idpatient,
                              })


def get_medication(request, id):
    try:
        medication = HistoryMedication.objects.get(pk=id)
    except HistoryMedication.DoesNotExist:
        raise Http404

    # get history information
    history = ListHistory.objects.get(pk=medication.id_history)
    patient = history.lastname
    numhistory = history.num_history
    dataset = Medication.objects.filter(id_key=id)
    return render_to_response('cconline/medication.html',
                              {
                                  'dataset': dataset,
                                  'num': numhistory,
                                  'patient': patient,
                                  'idpatient': medication.id_history,
                                  'medicname': medication.medic_name,
                              })