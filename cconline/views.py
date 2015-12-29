# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from models import Departments, ListHistory, ListDiary, ListAnalysis, LaboratoryData
from models import ActiveDepart, ListExamens, History, PatientInfo, HistoryMedication
from models import ListSurgery, SurgeryAdv, ListProffView, Medication, ListSpecialization
from models import RefExamens, ExamenDataset, ExamParam, ProfDataset
from models import SysUsers, UserGroups, Personal
from models import Diary
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.core.exceptions import PermissionDenied
from datetime import datetime
from django.db import connection
from forms import DiaryForm
from django.http import HttpResponseRedirect


def card_login(request, *args, **kwargs):
    """
    Авторизация, истечение срока сессии - 1 день
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(86400)
    return login(request, *args, **kwargs)


def get_current_doctor(request):
    """
    ФИО пользователя КардиоКарты
    :param request:
    :return: ФИО пользователя
    """
    current_user = request.user.username.upper()
    card_user = SysUsers.objects.get(pk=current_user)
    return card_user.user_fullname


def get_user_depart(request):
    """
    Получить код отделения, к которому привязан пользователь
    :param request:
    :return:
    """
    current_user = request.user.username.upper()
    card_user = SysUsers.objects.get(pk=current_user)
    id_doctor = card_user.id_doctor
    try:
        person = Personal.objects.get(pk=id_doctor)
    except:
        raise Http404
    return person.id_depart


def get_current_doctor_id(request):
    """
    Код пользователя КардиоКарты
    :param request:
    :return:
    """
    current_user = request.user.username.upper()
    card_user = SysUsers.objects.get(pk=current_user)
    return card_user.id_doctor


def get_user_groups(request):
    """
    Список групп, доступных пользователю
    :param request:
    :return:
    """
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
    current_user = request.user.last_name + ' ' + request.user.first_name
    return render_to_response('cconline/index.html',
        {
            'current_doc': get_current_doctor(request),
            'current_user': current_user,
            'list_group': get_user_groups(request),
        },
        context_instance=RequestContext(request))


@login_required(login_url='/login')
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
                                      'current_place': where_find,
                                      'current_doc': get_current_doctor(request),
                                  })


@login_required(login_url='/login')
def profile(request):
    current_user = request.user.username.upper()
    return render_to_response('cconline/profile.html', {
        'user': request.user,
        },
        context_instance=RequestContext(request)
        )


@login_required(login_url='/login')
def get_my_patient(request):
    """
    Мои пациенты
    :param request:
    :return: Список найденных историй по выбранному врачу
    """
    current_user = request.user.username.upper()
    card_user = SysUsers.objects.get(pk=current_user)
    id_doctor = card_user.id_doctor
    current_doc = card_user.user_fullname
    patients = ListHistory.objects.filter(id_doctor=id_doctor).filter(Q(discharge__isnull=True) | Q(discharge__gte=datetime.today()))
    return render_to_response('cconline/patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
            'current_place': u'Мои пациенты',
        })


@login_required(login_url='/login')
def get_patient_first_view(request, idpatient):
    """
    Данные первичного осмотра пациента, закладка "Лечащий врач"
    :param request:
    :param idpatient: Код пациента
    :return:
    """
    patient = History.objects.get(pk=idpatient)
    first_view = PatientInfo.objects.filter(id_history=idpatient).filter(id_view=0)
    age = patient.get_age()
    return render_to_response('cconline/patient_firstview.html',
                       {
                           'patient': patient,
                           'first_view': first_view,
                           'age': age,
                           'current_doc': get_current_doctor(request),
                       })


@login_required(login_url='/login')
def patient_cure(request, idpatient):
    try:
        history = History.objects.get(pk=idpatient)
    except History.DoesNotExist:
        raise Http404
    blood_type = history.get_blood_type(history.id)
    return render_to_response('cconline/patient_info.html',
            {
                'patient': history,
                'blood': blood_type,
                'current_doc': get_current_doctor(request),
            })


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
def get_lab_list(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    labs = ListAnalysis.objects.filter(id_history=idpatient).order_by('-date_execute')
    return render_to_response('cconline/list_laboratory.html',
                              {
                                  'labs': labs,
                                  'history': history,
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
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
    try:
        history = ListHistory.objects.get(pk=lab.id_history)
    except ListHistory.DoesNotExist:
        raise Http404
    lab_result = LaboratoryData.objects.filter(id_assigned_anal=id).order_by('sort_pos')
    return render_to_response('cconline/laboratory.html',
                              {
                                  'history': history,
                                  'order': lab,
                                  'result': lab_result,
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
def get_active_departs(request):
    departs = ActiveDepart.objects.all()
    return render_to_response('cconline/departs.html',
                              {
                                  'departs': departs,
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
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
            'from_departs': True,
        })


@login_required(login_url='/login')
def new_examen(request):
    """
    Добавить назначенное обследование
    :param request:
    :return:
    """
    if request.method != 'POST':
        raise Http404
    id_history = request.POST['id_history']
    try:
        history = ListHistory.objects.get(pk=id_history)
    except ListHistory.DoesNotExist:
        raise Http404
    id_doctor = get_current_doctor_id(request)
    id_department = history.id_depart
    id_group_exam = request.POST['examens']
    planyear = request.POST['planyear']
    planmonth = request.POST['planmonth']
    planday = request.POST['planday']
    planhour = request.POST['planhour']
    planmin = request.POST['planmin']
    plandate = datetime(int(planyear), int(planmonth), int(planday), int(planhour), int(planmin), 0)
    dataset = ExamenDataset()
    dataset.id_history = id_history
    dataset.id_doctor = id_doctor
    dataset.id_department = id_department
    dataset.id_group_examenation = id_group_exam
    dataset.appointment_date = datetime.now()
    dataset.plan_date = plandate
    dataset.id_typepay = 0
    dataset.save()
    redirect_url = '/examens/list/' + id_history
    return render_to_response('cconline/redirect.html', {
        'message': u'Добавлено обследование',
        'redirect_url': redirect_url,
        'type_message': 'bg-info',
        'request': request,
        },
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def add_new_exam(request, idpatient):
    history = ListHistory.objects.get(pk=idpatient)
    examens = RefExamens.objects.all()
    return render_to_response('cconline/newexam.html', {
        'history': history,
        'exam_list': examens,
        'id': idpatient,
        'cur_month': datetime.today().month,
    },
    context_instance=RequestContext(request))


@login_required(login_url='/login')
def delete_exam(request, id_exam):
    try:
        examen = ListExamens.objects.get(pk=id)
    except ListExamens.DoesNotExist:
        raise Http404
    id_history = examen.id_history
    examen.delete()
    redirect_url = '/examens/list/' + str(id_history)
    return render(request,  'cconline/redirect.html', {'message': 'Обследование удалёно', 'type_message': 'bg-info', 'redirect_url': redirect_url, 'request': request})


@login_required(login_url='/login')
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
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
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

    params = ExamParam.objects.raw('select * from SP_EXAM_PARAM(%s)', [id])

    return render_to_response('cconline/examen.html',
                              {
                                  'examen': examen,
                                  'params': params,
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
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
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
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
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
def get_proview(request, id):
    """
    Данные проф. осмотра пациента
    :param request:
    :param id:Код проф. осмотра
    :return: Данные осмотра, с закладками
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
                                  'current_doc': get_current_doctor(request),
                              })


def add_new_prof(request, idpatient):
    """
    Добавление нового осмотра профильным специалистом
    :param request:
    :param idpatient: Код пациента
    :return:
    """
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    specs = ListSpecialization.objects.all().order_by('name')
    return render_to_response('cconline/new_prof.html', {
        'history': history,
        'spec_list': specs,
        'id': idpatient,
        'cur_month': datetime.today().month,
        },
        context_instance=RequestContext(request))


def save_prof(request):
    """
    Добавить проф. осмотр
    :param request:
    :return:
    """
    if request.method != 'POST':
        raise Http404
    id_history = request.POST.get('id_history', 0)
    try:
        history = ListHistory.objects.get(pk=id_history)
    except ListHistory.DoesNotExist:
        raise Http404
    id_doctor = get_current_doctor_id(request)
    id_department = history.id_depart
    id_spec = request.POST['specs']
    plan_year = request.POST['plan_date']
    plan_hour = request.POST['plan_time']
    format_dt = '%Y-%m-%d %H:%M'
    date_str = '%s %s' % (plan_year, plan_hour)
    try:
        plan_date = datetime.strptime(date_str, format_dt)
    except:
        redirect_url = '/proview/add/' + id_history
        return render_to_response('cconline/redirect.html', {
            'message': u'Некорректно указана дата назначения осмотра!',
            'redirect_url': redirect_url,
            'type_message': 'bg-danger',
            'request': request,
            },
            context_instance=RequestContext(request))

    dataset = ProfDataset()
    dataset.id_history = id_history
    dataset.id_doctor = id_doctor
    dataset.id_depart = id_department
    dataset.id_spec = id_spec
    dataset.assign_date = datetime.now()
    dataset.plan_date = plan_date
    dataset.save()
    redirect_url = '/proview/list/' + id_history
    return render_to_response('cconline/redirect.html', {
        'message': u'Добавлено обследование',
        'redirect_url': redirect_url,
        'request': request,
        'type_message': 'bg-info',
        },
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def get_operation(request, id):
    """
    Описание операции
    :param request:
    :param id: Код операции
    :return: Данные операции
    """
    avail_groups = get_user_groups(request)
    # докторам разрешен просмотр
    if ('DOCTOR' not in avail_groups) and (request.user.username.upper() != 'SYSDBA'):
        raise PermissionDenied
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
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
def get_list_medication(request, idpatient):
    """
    Список назначенных медикаментов
    :param request:
    :param idpatient: Код пациента
    :return: Список назначенных препаратов
    """
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
                                  'current_doc': get_current_doctor(request),
                              })


@login_required(login_url='/login')
def get_medication(request, id):
    """
    Назначение по дням/часам
    :param request:
    :param id: Код назначения
    :return: Список назначений одного препарата
    """
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
              'current_doc': get_current_doctor(request),
          })


@login_required(login_url='/login')
def prolong_medication(request, id):
    """
    Продлить назначение препарата
    :param request:
    :param id: Код назначения
    :return:
    """
    try:
        medication = Medication.objects.get(pk=id)
    except HistoryMedication.DoesNotExist:
        raise Http404

    # get history information
    history = ListHistory.objects.get(pk=medication.id_history)
    patient = history.lastname
    numhistory = history.num_history

    return render_to_response('cconline/prolong_medic.html', {
          'dataset': medication,
          'id': medication.id,
          'num': numhistory,
          'patient': patient,
          'current_doc': get_current_doctor(request),
          'cur_month': datetime.today().month,
    },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def prolong_med(request):
    """
    Продлить назначение препарата на период
    :param request:
    :return:
    """
    if request.method != 'POST':
        raise Http404

    id_medication = request.POST['id_medication']

    try:
        medication = Medication.objects.get(pk=id_medication)
    except HistoryMedication.DoesNotExist:
        raise Http404

    year1 = request.POST['planyear']
    month1 = request.POST['planmonth']
    day1 = request.POST['planday']

    year2 = request.POST['planyear2']
    month2 = request.POST['planmonth2']
    day2 = request.POST['planday2']

    date1 = "%d-%d-%d" % (int(year1), int(month1), int(day1))
    date2 = "%d-%d-%d" % (int(year2), int(month2), int(day2))

    id_medication = 0

    sql = "EXECUTE PROCEDURE SP_COPY_ASSIGN_MEDIC (%s, '%s', '%s')" % (id_medication, date1, date2)
    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        mess = u'Лечение продлено'
    except:
        mess = u'Ошибка продления лечения!'

    redirect_url = '/medication/' + str(medication.id_key)
    return render_to_response('cconline/redirect.html', {
        'message': mess,
        'redirect_url': redirect_url,
        'request': request,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def add_new_laboratory(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    return render_to_response('cconline/new_lab.html', {
        'history': history,
        'cur_month': datetime.today().month,
        },
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def get_diary(request, id_diary):
    """
    Дневник на просмотр
    :param request:
    :param id_diary: Код дневника
    :return:
    """
    try:
        diary = ListDiary.objects.get(pk=id_diary)
    except ListDiary.DoesNotExist:
        raise Http404
    try:
        history = ListHistory.objects.get(pk=diary.id_history)
    except ListHistory.DoesNotExist:
        raise Http404
    return render_to_response('cconline/diary.html',
                {
                  'diary': diary,
                  'history': history,
                  'current_doc': get_current_doctor(request),
                })


@login_required(login_url='/login')
def new_diary(request, idpatient):
    """
    Новый дневник пациента
    :param request:
    :return:
    """
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404

    id_doctor = get_current_doctor_id(request)
    id_depart = history.id_depart
    patient = history.lastname
    depart = history.depart_name
    form = DiaryForm(initial=
        {
            'patient': patient,
            'department': depart,
            'id_history': idpatient,
            'id_depart': id_depart,
            'id_doctor': id_doctor,
            'diary_date': datetime.today(),

         }
        )
    return render_to_response('cconline/edit_diary.html', {
        'form': form,
        'id_history': idpatient,
        },
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_diary(request, id_diary):
    try:
        diary = Diary.objects.get(pk=id_diary)
    except Diary.DoesNotExist:
        raise Http404
    diary_form = DiaryForm(instance=diary)
    return render(request,  'cconline/edit_diary.html', {'form': diary_form})


@login_required(login_url='/login')
def save_diary(request):
    if request.method != 'POST':
        raise Http404
    id_diary = request.POST.get('id', '')
    if id_diary != '':
        diary = Diary.objects.get(pk=id_diary)
        id_history = diary.id_history
        diary_form = DiaryForm(request.POST, instance=diary)
        if diary_form.is_valid():
            diary_form.save()
    else:
        diary_form = DiaryForm(request.POST)
        id_history = request.POST.get('id_history', 0)
        if diary_form.is_valid():
            diary_form.save()
    redirect_url = '/diary/list/' + id_history
    return render_to_response('cconline/redirect.html', {
        'message': diary_form.errors,
        'redirect_url': redirect_url,
        'request': request,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def delete_diary(request, id_diary):
    try:
        diary = Diary.objects.get(pk=id_diary)
    except Diary.DoesNotExist:
        raise Http404
    id_history = diary.id_history
    diary.delete()
    redirect_url = '/diary/list/' + str(id_history)
    return render(request,  'cconline/redirect.html', {
        'message': 'Дневник удалён',
        'redirect_url': redirect_url,
        'request': request,
        'type_message': 'bg-info',
    })


@login_required(login_url='/login')
def get_nurse_work(request):
    return render_to_response('cconline/nurse_work.html',
        {
            'id_depart': get_user_depart(request),
            'current_doc': get_current_doctor(request),
        }
        )