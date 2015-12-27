# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
import random
import views
from models import ListHistory
import json
from django.template.loader import get_template
from django.template import Context
from models import ListAllAnalysis, ListOfAnalysis, Templates, ListTemplates, NurseLabWork, NurseMedWork
from django.core import serializers
from django.db import connection
from datetime import datetime
from collections import namedtuple

MED_WORK = NurseMedWork


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
    is_local_net = ('192.168.1' in remote_address) or ('127.0.0.1' in remote_address)
    #if not is_local_net:
    #    raise Http404
    template = get_template('cconline/test.html')
    page_data = { 'REQ_META': request.META, 'is_local_net': is_local_net, }
    context = template.render(Context(page_data))
    return HttpResponse(context)


def page_not_found(request):
    # обработчик Страница не найден
    response = render_to_response('404.html',
                                  {},
                                  context_instance=RequestContext(request)
                                  )
    response.status_code = 404
    return response


def permission_denied(request):
    # обработчик Доступ запрещён
    response = render_to_response('403.html',
                                  {},
                                  context_instance=RequestContext(request)
                                  )
    response.status_code = 403
    return response


def server_error(request):
    # обработчик Ошибка сервера
    response = render_to_response('500.html',
                                  {},
                                  context_instance=RequestContext(request)
                                  )
    response.status_code = 500
    return response


def json_subtest(request):
    """
    Список саб-тестов для теста
    :param request:
    :return:
    """
    mtest = request.GET['q']
    tests = ListAllAnalysis.objects.filter(id_parent=mtest).order_by('name')
    data = serializers.serialize('json', tests)
    return HttpResponse(data, mimetype='application/json')


def json_test(request):
    """
    Список основных тестов
    :param request:
    :return:
    """
    dataset = ListOfAnalysis.objects.all()
    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')


def json_savetest(request):
    """
    Сохранить назначение анализа
    :param request:
    :return: Перенаправление на страницу
    """
    if request.method == 'POST':
        json_data = request.body
        params = json.loads(json_data)
        id_doctor = views.get_current_doctor_id(request)
        id_history = params['id_history']
        id_test = params['pk']
        sub_tests = params['selected']
        plan_year = int(params['plan_year'])
        plan_month = int(params['plan_month'])
        plan_day = int(params['plan_day'])
        plan_hour = int(params['plan_hour'])
        plan_min = int(params['plan_min'])
        assign_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        plan_date = datetime(plan_year, plan_month, plan_day, plan_hour, plan_min)
        is_cito = params['is_cito']

        try:
            history = ListHistory.objects.get(pk=id_history)
        except ListHistory.DoesNotExist:
            raise Http404
        id_depart = history.id_depart
        sql = "SELECT ID FROM SP_REG_LABTEST (%s, %s, %s, '%s', '%s', '%s', %s)" \
              % (id_history, id_doctor, id_depart, id_test, assign_date, plan_date, is_cito)
        cursor = connection.cursor()
        cursor.execute(sql)
        results = named_tuple_fetch_all(cursor)
        id_order = results[0][0]
        connection.commit()

        # Добавить сабтесты для анализа
        for sub_test in sub_tests:
            sql = "EXECUTE PROCEDURE SP_ASSIGN_ANALYSIS (%s, %s, %s)" % (id_order, sub_test, is_cito)
            cursor = connection.cursor()
            cursor.execute(sql)
        connection.commit()

        redirect_url = 'laboratory/list/' + id_history
        response = render_to_response('cconline/redirect.html', {
            'message': u'Добавлен анализ' + str(id_order),
            'redirect_url': redirect_url,
            'request': request,
        },
            context_instance=RequestContext(request)
        )
        response.status_code = 200
        return response


def named_tuple_fetch_all(cursor):
    # "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def json_templates(request):
    """
    Список шаблонов или шаблон
    :param request:
    GET - "g" - list template by Group
          "id" - get template by Id
    :return:
    """
    id_group = request.GET.get('g', '')
    id = request.GET.get('id', '')
    if (id_group == '') and (id == ''):
        raise Http404
    if id_group != '':
        templates = ListTemplates.objects.filter(id_template=id_group).filter(id_type=0)
    elif id != '':
        templates = Templates.objects.filter(id=id)
    data = serializers.serialize('json', templates)
    return HttpResponse(data, mimetype='application/json')


def json_nurse_lab(request):
    import datetime
    """

    :param request:
    :return:
    """
    id_depart = request.GET.get('d', '')
    period = request.GET.get('p', '')
    if period == '':
        raise Http404
    now = '2015-12-11'  # datetime.date.today().strftime("%Y-%m-%d")
    tomorrow = '2015-12-12'  # now + datetime.timedelta(1).strftime("%Y-%m-%d")

    if period == 'today':
        start_date = now # + ' 00:00:00'
        end_date = now # + ' 23:59:59'
    elif period == 'tomorrow':
        start_date = tomorrow + ' 00:00'
        end_date = tomorrow + ' 23:59:59'
    dataset = NurseLabWork.objects.filter(id_depart=id_depart).filter(date_plan=start_date)
    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')


def json_nurse_med(request):
    import datetime
    """

    :param request:
    :return:
    """
    id_depart = request.GET.get('d', '')
    period = request.GET.get('p', '')
    if period == '':
        raise Http404
    now = '2015-12-11'  # datetime.date.today().strftime("%Y-%m-%d")
    tomorrow = '2015-12-12'  # now + datetime.timedelta(1).strftime("%Y-%m-%d")

    if period == 'today':
        start_date = now # + ' 00:00:00'
        end_date = now # + ' 23:59:59'
    elif period == 'tomorrow':
        start_date = tomorrow + ' 00:00'
        end_date = tomorrow + ' 23:59:59'
    dataset = NurseMedWork.objects.filter(id_depart=id_depart).filter(date_plan=start_date)
    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')