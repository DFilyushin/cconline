# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
import random
import views
from models import ListHistory
import json
import string
from django.template.loader import get_template
from django.template import Context
from models import ListAllAnalysis, ListOfAnalysis, Templates, ListTemplates, NurseAssign
from models import NurseLabWork, NurseMedWork, NurseExamWork, NurseProfViewWork
from django.core import serializers
from django.db import connection
from datetime import datetime
from collections import namedtuple
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from django.contrib import auth



MED_WORK = NurseMedWork


def getpass(request):
    # create pass sha256 for client ;-)
    remote_address = request.META['REMOTE_ADDR']
    is_local_net = ('192.168.1' in remote_address) or ('127.0.0.1' in remote_address)
    if not is_local_net:
        raise Http404
    user_pass = request.GET.get('pass')
    salt = request.GET.get('salt', '-')
    if not user_pass:
        raise Http404
    if salt == '-':
        salt = str(random.randint(1000, 9000))
    password = make_password(user_pass, salt, 'pbkdf2_sha256')
    return HttpResponse(password, mimetype='text/html')


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


def change_password(request):
    current_user = request.user.last_name + ' ' + request.user.first_name
    if request.method == 'GET':
        return render_to_response('registration/password_change_form.html', {
            'current_user': current_user,
            },
            context_instance=RequestContext(request))
    else:
        old_pass = request.POST.get('old_password', '')
        pass1 = request.POST.get('new_password1', '')
        pass2 = request.POST.get('new_password2', '')
        if pass1 == pass2:
            user = User.objects.get(username__exact=request.user.username)
            user.set_password(pass1)
            user.save()

        response = render_to_response('cconline/redirect.html', {
            'message': u'Пароль изменён',
            'redirect_url': '/',
            'request': request,
        },
            context_instance=RequestContext(request)
        )
        response.status_code = 200
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
    if request.method != 'POST':
        raise Http404

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
    """
    Return all rows from a cursor as a namedtuple
    :param cursor:
    :return:
    """
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
    id_template = request.GET.get('id', '')
    if (id_group == '') and (id_template == ''):
        raise Http404
    if id_group != '':
        templates = ListTemplates.objects.filter(id_template=id_group).filter(id_type=0)
    elif id != '':
        templates = Templates.objects.filter(id=id_template)
    data = serializers.serialize('json', templates)
    return HttpResponse(data, mimetype='application/json')


def json_nurse_lab(request):
    import datetime
    """
    Список назначений на лабораторные анализы для м/с
    :param request:
    :return:
    """
    id_depart = views.get_user_depart(request)
    period = request.GET.get('p', '')
    if period == '':
        raise Http404
    now = datetime.date.today()
    yesterday = (now + datetime.timedelta(-1)).strftime("%Y-%m-%d")
    tomorrow = (now + datetime.timedelta(1)).strftime("%Y-%m-%d")

    start_date = now.strftime("%Y-%m-%d")
    if period == 'tomorrow':
        start_date = tomorrow
    elif period == 'yesterday':
        start_date = yesterday
    dataset = NurseLabWork.objects.filter(id_depart=id_depart).filter(date_plan=start_date)
    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')


def json_nurse_med(request):
    """
    Список назначений препаратов пациенту для м/с
    :param request:
    :return:
    """
    import datetime
    id_depart = views.get_user_depart(request)
    period = request.GET.get('p', '')
    if period == '':
        raise Http404
    now = datetime.date.today()
    yesterday = (now + datetime.timedelta(-1)).strftime("%Y-%m-%d")
    tomorrow = (now + datetime.timedelta(1)).strftime("%Y-%m-%d")

    start_date = now.strftime("%Y-%m-%d")
    if period == 'tomorrow':
        start_date = tomorrow
    elif period == 'yesterday':
        start_date = yesterday
    dataset = NurseMedWork.objects.filter(id_depart=id_depart).filter(date_plan=start_date).\
        order_by('datetime_plan', 'medic_name')
    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')


def json_nurse_exam(request):
    """
    Список назначений обследований пациента для м/с
    :param request:
    :return:
    """
    import datetime
    id_depart = views.get_user_depart(request)
    period = request.GET.get('p', '')
    if period == '':
        raise Http404
    now = datetime.date.today()
    yesterday = (now + datetime.timedelta(-1)).strftime("%Y-%m-%d")
    tomorrow = (now + datetime.timedelta(1)).strftime("%Y-%m-%d")

    start_date = now.strftime("%Y-%m-%d")
    if period == 'tomorrow':
        start_date = tomorrow
    elif period == 'yesterday':
        start_date = yesterday
    dataset = NurseExamWork.objects.filter(id_depart=id_depart).filter(date_plan=start_date).\
        order_by('datetime_plan', 'exam')
    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')


def json_nurse_doctor(request):
    """
    Список назначений проф. осмотров пациента для м/с
    :param request:
    :return:
    """
    import datetime
    id_depart = views.get_user_depart(request)
    period = request.GET.get('p', '')
    if period == '':
        raise Http404
    now = datetime.date.today()
    yesterday = (now + datetime.timedelta(-1)).strftime("%Y-%m-%d")
    tomorrow = (now + datetime.timedelta(1)).strftime("%Y-%m-%d")
    start_date = now.strftime("%Y-%m-%d")
    if period == 'tomorrow':
        start_date = tomorrow
    elif period == 'yesterday':
        start_date = yesterday
    dataset = NurseProfViewWork.objects.filter(id_depart=id_depart).\
        filter(date_plan=start_date).order_by('datetime_plan', 'spec')
    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')


def nurse_execute(request):
    """
    Выполнение мед. назначений мед. сестрой
    :param request: POST через json
        t - тип назначения
        id - код записи
    :return:
    """
    if request.method != 'POST':
        raise Http404
    json_data = request.body
    params = json.loads(json_data)
    type_execute = params['t']
    id_record = params['id']
    id_nurse = views.get_current_doctor_id(request)
    assign_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = "EXECUTE PROCEDURE SP_NURSE_EXECUTE(%s, %s, %s, '%s')" % (type_execute, id_record, id_nurse, assign_date)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    return HttpResponse('200 Ok')


def nurse_work_by_patient(request):
    """
    Список работ по истории болезни
    :param request:
    :return:
    """
    id_patient = request.GET.get('id', 0)
    period = request.GET.get('period', 'today')

    sql = "SELECT * FROM GET_LIST_NURSE_MEDICATION(%s, '%s', %s, %s)" % (id_patient, period, 0, 0)

    dataset = NurseAssign.objects.raw(sql)

    data = serializers.serialize('json', dataset)
    return HttpResponse(data, mimetype='application/json')


class ValidatingPasswordChangeForm(auth.forms.PasswordChangeForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # Минимальная длина пароля
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        # Должен содержать символы верхнего и нижнего регистра, цифры, спец.символы
        have_digit = any(c.isdigit() for c in password1)
        have_upper = any(c.isupper() for c in password1)
        have_super = any(c in string.punctuation for c in password1)
        if not have_digit:
            raise forms.ValidationError("Пароль должен содержать цифры!")
        if not have_super:
            raise forms.ValidationError("Пароль должен содержать специальные символы")
        if not have_upper:
            raise forms.ValidationError("Пароль должен содержать символы верхнего и нижнего регистра")

        return password1
