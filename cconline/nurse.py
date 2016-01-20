# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response
from django.db.models import Q
from datetime import datetime
from models import ListHistory
from models import TemperatureList, NurseViewList, PainStatusList, RiskDownList
from models import TemperatureData, RiskDownData, PainStatus
from views import get_current_doctor, get_user_depart, get_user_groups, get_user_depart_name
from django.core.exceptions import PermissionDenied


@login_required(login_url='/login')
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
    return render_to_response('cconline/nurse.html', {
              'temp_list': temp_list,
              'view_list': view_list,
              'pain_list': pain_list,
              'down_list': down_list,
              'patient': patient,
              'num': numhistory,
              'idpatient': idpatient,
              'current_doc': get_current_doctor(request),
        })


@login_required(login_url='/login')
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
                           'current_doc': get_current_doctor(request),
                       })


@login_required(login_url='/login')
def get_risk_down(request, id):
    try:
        view = RiskDownData.objects.get(pk=id)
    except RiskDownData.DoesNotExist:
        raise Http404

    return render_to_response('cconline/risk_down.html',
                              {
                                  'view': view,
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
def get_pain_status(request, id):
    try:
        view = PainStatus.objects.get(pk=id)
    except PainStatus.DoesNotExist:
        raise Http404

    return render_to_response('cconline/pain_status.html',
                              {
                                  'view': view,
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
def get_nurse_work(request):
    """
    Сестринский журнал выполнения мед. назначений
    :param request:
    :return:
    """
    list_group = get_user_groups(request)
    if 'NURSE' not in list_group:
        raise PermissionDenied
    return render_to_response('cconline/nurse_work.html',
        {
            'id_depart': get_user_depart(request),
            'current_doc': get_current_doctor(request),
        }
        )


@login_required(login_url='/login')
def get_nurse_patients(request):
    """

    :param request:
    :return:
    """
    id_depart = get_user_depart(request)
    depart = get_user_depart_name(request)
    patients = ListHistory.objects.filter(id_depart=id_depart).\
        filter(Q(discharge__isnull=True) | Q(discharge__gte=datetime.today()))
    return render_to_response(
        'cconline/nurse_patients.html',
        {
            'depart': depart,
            'patients': patients,
        }
    )


@login_required(login_url='/login')
def get_nurse_patient(request, id):
    """

    :param request:
    :return:
    """
    try:
        history = ListHistory.objects.get(pk=id)
    except ListHistory.DoesNotExist:
        raise Http404

    return render_to_response(
        'cconline/nurse_patient.html',
        {
            'history': history,
        }
    )
