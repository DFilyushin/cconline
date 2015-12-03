from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import ListHistory
from models import TemperatureList, NurseViewList, PainStatusList, RiskDownList
from models import TemperatureData, RiskDownData, PainStatus
from views import get_current_doctor, get_current_doctor_id


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
    return render_to_response('cconline/nurse.html',
                              {
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

