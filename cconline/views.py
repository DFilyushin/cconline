# -*- coding: utf-8 -*-

from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import datetime, date
from forms import DiaryForm
from models import Departments, ListHistory, ListDiary, ListAnalysis, LaboratoryData, \
    ActiveDepart, ListExamens, History, PatientInfo, HistoryMedication, \
    ListSurgery, SurgeryAdv, ListProffView, Medication, ListSpecialization,\
    RefExamens, ExamenDataset, ExamParam, ProfDataset, \
    SysUsers, UserGroups, Personal, Diary, Hospitalization, HistoryMove, MedicationDates
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.views.decorators.cache import cache_page
import datetime


def card_login(request, *args, **kwargs):
    """
    Авторизация, истечение срока сессии - 1 день
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    if request.method == 'POST':
        f = AuthenticationForm(request, data=request.POST)
        if f.is_valid():
            last_user = request.POST.get('username', '')
            auth_login(request, f.get_user())
            response = HttpResponseRedirect('/')
            response.set_cookie('last_user', last_user)
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(86400)
            return response
    else:
        last_user = ''
        if request.COOKIES.has_key('last_user'):
            last_user = request.COOKIES['last_user']
        f = AuthenticationForm(initial={'username': last_user})
    return render(request, 'registration/login.html', {'form': f})


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


def get_user_depart_name(request):
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
    return person.depart


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
    id_depart = get_user_depart(request)
    return render_to_response(
        'cconline/index.html',
        {
            'current_doc': get_current_doctor(request),
            'current_user': current_user,
            'list_group': get_user_groups(request),
            'id_depart': id_depart,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def search(request):
    """
    Результаты поиска по номеру истории, ФИО пациента
    :param request:
    :return: Список найденных историй болезни
    """
    if request.method == "POST":
        find_string = request.POST['patient']
        patients = ListHistory.objects.filter(Q(num_history__startswith=find_string) | Q(lastname__iexact=find_string))\
            .order_by('receipt')
        where_find = mark_safe(u"Результаты поиска по <em>" + find_string + "</em>")
        return render_to_response(
            'cconline/patients.html',
            {
                'patients': patients,
                'current_place': where_find,
                'current_doc': get_current_doctor(request),
            }
        )
    else:
        raise Http404


@login_required(login_url='/login')
def profile(request):
    return render_to_response(
        'cconline/profile.html',
        {
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
    patients = ListHistory.objects.filter(id_doctor=id_doctor).\
        filter(Q(discharge__isnull=True) | Q(discharge__gte=datetime.today())).\
        order_by('-receipt')
    return render_to_response(
        'cconline/patients.html',
        {
            'current_doc': current_doc,
            'patients': patients,
            'current_place': u'Мои пациенты',
        }
    )


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
    return render_to_response(
        'cconline/patient_firstview.html',
        {
            'patient': patient,
            'first_view': first_view,
            'age': age,
            'current_doc': get_current_doctor(request),
        }
    )


@login_required(login_url='/login')
def patient_cure(request, idpatient):
    try:
        history = History.objects.get(pk=idpatient)
    except History.DoesNotExist:
        raise Http404
    movement = HistoryMove.objects.filter(id_history=idpatient).order_by('datemove')
    blood_type = history.get_blood_type(history.id)

    return render_to_response(
        'cconline/patient_info.html',
        {
            'patient': history,
            'movement': movement,
            'blood': blood_type,
            'current_doc': get_current_doctor(request),
        }
    )


@login_required(login_url='/login')
@cache_page(60 * 5)
def get_patient(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404

    return render_to_response(
        'cconline/patient.html',
        {
            'history': history,
            'current_doc': get_current_doctor(request),
            'list_group': get_user_groups(request),
        }
    )


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
    return render_to_response(
        'cconline/list_diary.html',
        {
            'diarys': diarys,
            'history': history,
            'current_doc': get_current_doctor(request),
        }
    )


@login_required(login_url='/login')
def get_lab_list(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    labs = ListAnalysis.objects.filter(id_history=idpatient).order_by('-date_execute')
    return render_to_response(
        'cconline/list_laboratory.html',
        {
            'labs': labs,
            'history': history,
            'current_doc': get_current_doctor(request),
            'list_group': get_user_groups(request),
        }
    )


@login_required(login_url='/login')
def get_laboratory(request, id):
    """
    Данные одного лабораторного анализа
    :param request:
    :param id: Код анализа (pk)
    :return:
    """
    id_depart = get_user_depart(request)
    try:
        lab = ListAnalysis.objects.get(pk=id)
    except ListAnalysis.DoesNotExist:
        raise Http404
    try:
        history = ListHistory.objects.get(pk=lab.id_history.id)
    except ListHistory.DoesNotExist:
        raise Http404
    lab_result = LaboratoryData.objects.filter(id_assigned_anal=id).order_by('sort_pos')
    return render_to_response(
        'cconline/laboratory.html',
        {
            'history': history,
            'order': lab,
            'result': lab_result,
            'current_doc': get_current_doctor(request),
            'id_depart': id_depart,
        }
    )


@login_required(login_url='/login')
@cache_page(60 * 15)
def get_active_departs(request):
    departs = ActiveDepart.objects.all()
    return render_to_response(
        'cconline/departs.html',
        {
            'departs': departs,
            'current_doc': get_current_doctor(request),
        }
    )


@login_required(login_url='/login')
@cache_page(60 * 5)
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
    cur_date = datetime.datetime.now()
    patients = ListHistory.objects.filter(id_depart=iddepart).\
        filter(Q(discharge__gt=cur_date) | Q(discharge__isnull=True)).order_by('-receipt')
    return render_to_response(
        'cconline/patients.html',
        {
            'patients': patients,
            'current_place': depart.name,
            'current_doc': get_current_doctor(request),
            'from_departs': True,
            'year': cur_date.year.__str__(),
        }
    )


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
    plandate = datetime.datetime(int(planyear), int(planmonth), int(planday), int(planhour), int(planmin), 0)

    dataset = ExamenDataset()
    dataset.id_history = id_history
    dataset.id_doctor = id_doctor
    dataset.id_department = id_department
    dataset.id_group_examenation = id_group_exam
    dataset.appointment_date = datetime.datetime.now()
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
    return render_to_response(
        'cconline/new_exam.html',
        {
            'history': history,
            'exam_list': examens,
            'id': idpatient,
            'cur_month': datetime.datetime.today().month,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def delete_exam(request, id_exam):
    try:
        examen = ListExamens.objects.get(pk=id)
    except ListExamens.DoesNotExist:
        raise Http404
    id_history = examen.id_history
    examen.delete()
    redirect_url = '/examens/list/' + str(id_history)
    return render(request,  'cconline/redirect.html', {
        'message': 'Обследование удалёно',
        'type_message': 'bg-info',
        'redirect_url': redirect_url,
        'request': request
        }
                  )


@login_required(login_url='/login')
def get_examen_list(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    examens = ListExamens.objects.filter(id_history=idpatient).order_by('-date_plan')
    return render_to_response('cconline/list_examens.html',
        {
            'examens': examens,
            'history': history,
            'current_doc': get_current_doctor(request),
            'list_group': get_user_groups(request),
        }
    )


@login_required(login_url='/login')
def get_examen(request, id):
    """
    Данные обследования
    :param request:
    :param id: Код обследования (pk)
    :return:
    """
    id_depart = get_user_depart(request)
    try:
        examen = ListExamens.objects.get(pk=id)
    except ListExamens.DoesNotExist:
        raise Http404
    params = ExamParam.objects.raw('select * from SP_EXAM_PARAM(%s)', [id])
    return render_to_response(
        'cconline/examen.html',
        {
            'examen': examen,
            'params': params,
            'list_group': get_user_groups(request),
            'current_doc': get_current_doctor(request),
            'id_depart': id_depart,
        }
    )


@login_required(login_url='/login')
def get_list_surgery(request, idpatient):
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    surgery = ListSurgery.objects.filter(id_history=idpatient).order_by('surgery_date')
    return render_to_response(
        'cconline/list_surgery.html',
        {
            'surgery': surgery,
            'history': history,
            'current_doc': get_current_doctor(request),
        }
    )


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
    dataset = ListProffView.objects.filter(id_history=idpatient)
    return render_to_response(
        'cconline/list_prof_view.html',
        {
            'history': history,
            'proflist': dataset,
            'current_doc': get_current_doctor(request),
        }
    )


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
    return render_to_response(
        'cconline/proview.html',
        {
            'proview': proview,
            'pages': pages,
            'idpatient': proview.id_history,
            'num': proview.num_history,
            'patient': proview.patient,
            'current_doc': get_current_doctor(request),
        }
    )


@login_required(login_url='/login')
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
    return render_to_response(
        'cconline/new_prof.html',
        {
            'history': history,
            'spec_list': specs,
            'cur_month': datetime.datetime.today().month,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
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
        plan_date = datetime.datetime.strptime(date_str, format_dt)
    except:
        redirect_url = '/proview/add/' + id_history
        return render_to_response(
            'cconline/redirect.html',
            {
                'message': u'Некорректно указана дата назначения осмотра!',
                'redirect_url': redirect_url,
                'type_message': 'bg-danger',
                'request': request,
            },
            context_instance=RequestContext(request)
        )

    dataset = ProfDataset()
    dataset.id_history = id_history
    dataset.id_doctor = id_doctor
    dataset.id_depart = id_department
    dataset.id_spec = id_spec
    dataset.assign_date = datetime.datetime.now()
    dataset.plan_date = plan_date
    dataset.save()
    redirect_url = '/proview/list/' + id_history
    return render_to_response(
        'cconline/redirect.html',
        {
            'message': u'Назначен осмотр профильным специалистом',
            'redirect_url': redirect_url,
            'request': request,
            'type_message': 'bg-info',
        },
        context_instance=RequestContext(request)
    )


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
    if 'DOCTOR' not in avail_groups:
        raise PermissionDenied
    try:
        operation = ListSurgery.objects.get(pk=id)
    except ListSurgery.DoesNotExist:
        raise Http404
    adv_info = ''
    if operation.type_operation == 1:
        advanced = SurgeryAdv.objects.filter(id_surgery=id).filter(id_type=9)
        adv_info = advanced[0].text_value
    return render_to_response(
        'cconline/operation.html',
        {
            'operation': operation,
            'adv_info': adv_info,
        }
    )


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
    dataset = HistoryMedication.objects.filter(id_history=idpatient)
    return render_to_response(
        'cconline/list_medication.html',
        {
            'dataset': dataset,
            'history': history,
            'current_doc': get_current_doctor(request),
        }
    )


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
    cur_date = datetime.datetime.now()
    # get history information
    history = ListHistory.objects.get(pk=medication.id_history)
    dataset = Medication.objects.filter(id_key=id)
    return render_to_response(
        'cconline/medication.html',
        {
            'dataset': dataset,
            'history': history,
            'medicname': medication.medic_name,
            'current_doc': get_current_doctor(request),
            'year': cur_date.year.__str__(),
            'list_group': get_user_groups(request),

        }
    )


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

    return render_to_response(
        'cconline/prolong_medic.html',
        {
            'dataset': medication,
            'history': history,
            'id': medication.id,
            'current_doc': get_current_doctor(request),
            'cur_month': datetime.datetime.today().month,
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
    list_group = get_user_groups(request)
    if 'DOCTOR' not in list_group:
        raise PermissionDenied
    id_medication = request.POST.get('id_medication', 0)
    if id_medication == 0:
        raise Http404

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

    sql = "EXECUTE PROCEDURE SP_COPY_ASSIGN_MEDIC (%s, '%s', '%s')" % (id_medication, date1, date2)
    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        connection.commit()
        mess = u'Лечение продлено'
    except:
        mess = u'Ошибка продления лечения!'

    redirect_url = '/medication/' + str(medication.id_key)
    return render_to_response(
        'cconline/redirect.html',
        {
            'message': mess,
            'redirect_url': redirect_url,
            'request': request,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def add_new_laboratory(request, idpatient):
    """
    Добавление нового анализа
    :param request:
    :param idpatient: Код пациента
    :return:
    """
    list_group = get_user_groups(request)
    if 'DOCTOR' not in list_group:
        raise PermissionDenied

    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    return render_to_response(
        'cconline/new_lab.html',
        {
            'history': history,
            'cur_month': datetime.datetime.today().month,
        },
        context_instance=RequestContext(request)
    )


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
    return render_to_response(
        'cconline/diary.html',
        {
            'diary': diary,
            'history': history,
            'current_doc': get_current_doctor(request),
        }
    )


@login_required(login_url='/login')
def new_diary(request, idpatient):
    """
    Новый дневник пациента
    :param request:
    :param idpatient: patient code
    :return:
    """
    list_group = get_user_groups(request)
    if 'DOCTOR' not in list_group:
        raise PermissionDenied
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404

    form = DiaryForm(initial=
        {
            'patient': history.lastname,
            'department': history.depart_name,
            'id_history': idpatient,
            'id_depart': history.id_depart,
            'id_doctor': get_current_doctor_id(request),
            'diary_date': datetime.datetime.today(),
        }
    )
    return render_to_response(
        'cconline/edit_diary.html',
        {
            'form': form,
            'id_history': idpatient,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def edit_diary(request, id_diary):
    try:
        diary = Diary.objects.get(pk=id_diary)
    except Diary.DoesNotExist:
        raise Http404
    diary_form = DiaryForm(instance=diary)
    return render(
        request,
        'cconline/edit_diary.html',
        {
            'form': diary_form
        }
    )


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
    """
    Удаление дневника
    :param request:
    :param id_diary: Код дневника
    :return:
    """
    list_group = get_user_groups(request)
    if 'DOCTOR' not in list_group:
        raise PermissionDenied
    try:
        diary = Diary.objects.get(pk=id_diary)
    except Diary.DoesNotExist:
        raise Http404
    id_history = diary.id_history
    diary.delete()
    redirect_url = '/diary/list/' + str(id_history)
    return render(request,  'cconline/redirect.html', {
        'message': u'Дневник удалён',
        'redirect_url': redirect_url,
        'request': request,
        'type_message': 'bg-info',
    })


@login_required(login_url='/login')
@cache_page(60 * 15)
def stat(request):
    """
    Статистика
    :param request:
    :return:
    """
    list_depart = ActiveDepart.objects.all().order_by('name')  # количество пациентов по отделениям
    hospitalization = Hospitalization.objects.all()  # госпитализация по отделениям
    return render_to_response(
        'cconline/stat.html',
        {
            'departs': list_depart,
            'hospit': hospitalization,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def add_doctor_view(request, idpatient):
    """
    Добавление новой записи осмотра с выбором вида осмотра
    :param request:
    :param idpatient: Код пациента
    :return:
    """

    rst_unused = PatientInfo.get_non_existent_view(idpatient)
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404

    return render_to_response(
        'cconline/edit_view.html',
        {
            'listpages': rst_unused,
            'id': 0,
            'doctor_page_title': 'Добавление новой записи',
            'id_param': 0,
            'id_history': idpatient,
            'text': '',
            'history': history,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def get_doctor_view(request, idpatient, idparam):
    """
    Изменение записи по первичному осмотру пациента
    :param request:
    :return:
    """

    # Обработка ошибок пока исключена !!!
    data_view = PatientInfo.objects.filter(id_history=idpatient).filter(id_view=0).filter(id_param=idparam)
    try:
        history = ListHistory.objects.get(pk=idpatient)
    except ListHistory.DoesNotExist:
        raise Http404
    return render_to_response(
        'cconline/edit_view.html',
        {
            'id': data_view[0].id,
            'doctor_page_title': data_view[0].param_name,
            'id_param': data_view[0].id_param,
            'id_history': data_view[0].id_history,
            'text': data_view[0].text,
            'history': history,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def save_prof_conclusion(request):
    """
    Сохранить изменения в заключении проф. осмотра
    :param request:
    :return:
    """
    id = request.POST.get('id', 0)
    id_doctor = get_current_doctor_id(request)
    date_exec = request.POST.get('dateexec', '')
    time_exec = request.POST.get('timeexec', '')
    conclusion = request.POST.get('view_text', '')
    datetime_exec = date_exec + ' ' + time_exec
    try:
        dataset = ListProffView.objects.get(pk=id)
        dataset.conclusion = conclusion
        dataset.id_doctor = id_doctor
        dataset.viewdate = datetime_exec
        dataset.save()
    except ListProffView.DoesNotExist:
        raise Http404

    redirect_url = '/proview/list/' + str(dataset.id_history)
    return render_to_response(
        'cconline/redirect.html',
        {
            'message': u'Изменения сохранены...',
            'redirect_url': redirect_url,
            'request': request,
            'type_message': 'bg-info',
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def edit_prof_conclusion(request, id):
    """
    Редактирование проф. осмотра, ввод заключения
    :param request:
    :param id:
    :return:
    """
    text_value = ''
    try:
        dataset = ListProffView.objects.get(pk=id)
        text_value = dataset.conclusion
        if dataset.viewdate:
            cur_date = dataset.viewdate.strftime('%Y-%m-%d')
            cur_time = dataset.viewdate.strftime('%H:%M')
            doctor = dataset.doctor
        else:
            cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
            cur_time = datetime.datetime.now().strftime('%H:%M')
            doctor = get_current_doctor(request)

    except ListProffView.DoesNotExist:
        raise Http404
    id_history = dataset.id_history
    try:
        history = ListHistory.objects.get(pk=id_history)
    except ListHistory.DoesNotExist:
        raise Http404

    return render_to_response(
        'cconline/edit_prof_view.html',
        {
            'id': id,
            'history': history,
            'spec_doctor': dataset.specname,
            'doctor': doctor,
            'text': text_value,
            'date_exec': cur_date,
            'time_exec': cur_time,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def save_doctor_view(request):
    """

    Запись изменений по осмотру пациента (отдельная вкладка лечащего врача)

    """
    if request.method != 'POST':
        raise Http404
    id = request.POST.get('id', 0)
    id_history = request.POST.get('id_history', 0)

    if id == '0':
        id_param = request.POST.get('selected_title', 0)
    else:
        id_param = request.POST.get('id_param', 0)
    text_view = request.POST.get('view_text', '')

    redirect_url = '/patient/first_view/' + id_history

    # проверка уникальности записей

    if (id == '0') and not PatientInfo.check_uniq_param(id_history, id_param):
        return render_to_response(
            'cconline/redirect.html',
            {
                'message': u'Запись уже имеется у пациента...',
                'redirect_url': redirect_url,
                'request': request,
                'type_message': 'bg-warning',
            },
            context_instance=RequestContext(request)
        )

    if id == '0':
        dataset = PatientInfo()
    else:
        dataset = PatientInfo.objects.get(pk=id)
    dataset.text = text_view
    dataset.id_history = id_history
    dataset.id_param = id_param
    dataset.id_view = 0
    dataset.save()

    return render_to_response(
        'cconline/redirect.html',
        {
            'message': u'Изменения сохранены...',
            'redirect_url': redirect_url,
            'request': request,
            'type_message': 'bg-info',
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def choose_test(request):
    id_depart = get_user_depart(request)
    try:
        name_depart = Departments.objects.get(pk=id_depart).name
    except Departments.DoesNotExist:
        name_depart = u'не указано отделение'
    return render_to_response(
        'cconline/actual_result.html',
        {
            'id_depart': id_depart,
            'depart': name_depart,
        }, context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
@cache_page(60 * 5)
def last_exam(request, iddepart):
    """
    Get last 30 ready examenation by department of doctor
    :param request:
    :return:
    """
    examenation_test = ListExamens.objects.filter(id_depart=iddepart).filter(date_execute__isnull=False)\
                           .order_by('-date_execute')[:30]
    return render_to_response(
        'cconline/last_examenation.html',
        {
            'exams': examenation_test,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
@cache_page(60 * 5)
def last_lab(request, iddepart):
    """
    Get last 30 ready laboratory by department of doctor
    :param request:
    :return:
    """
    laboratory_test = ListAnalysis.objects.filter(id_depart=iddepart).filter(date_execute__isnull=False)\
                          .order_by('-date_execute')[:30]
    return render_to_response(
        'cconline/last_laboratory.html',
        {
            'labs': laboratory_test,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/login')
def get_list_medication_by_date(request, idpatient):
    """
    Get list medication by dates, view all date with assigned medication
    :param request:
    :param idpatient:
    :return:
    """
    current_year = request.GET.get('year', 0)
    current_month = request.GET.get('month', 0)
    if (current_year == 0) or (current_month == 0):
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

    list_dates = MedicationDates.objects.filter(id_history=idpatient).filter(year=current_year)\
        .filter(month=current_month)
    if not list_dates.exists():
        list_dates = MedicationDates.objects.filter(id_history=idpatient)
        current_year = list_dates[0].year
        current_month = list_dates[0].month
        list_dates = MedicationDates.objects.filter(id_history=idpatient).filter(year=current_year)\
            .filter(month=current_month)
        show_prev = False
        show_next = True
    else:
        show_next = True
        show_prev = True
    return render_to_response('cconline/list_medication_by_dates.html',
        {
            'month': current_month,
            'year': current_year,
            'event_list': list_dates,
            'show_next': show_next,
            'show_prev': show_prev,
        },
        context_instance=RequestContext(request)
    )


def get_medication_by_date(request, idpatient, date_assign):
    """

    :param request:
    :param idpatient:
    :param date_assign:
    :return:
    """
    date1 = datetime.datetime.strptime(date_assign, '%Y-%m-%d')
    date2 = datetime.datetime.combine(date1, datetime.time.max)

    medication = Medication.objects.filter(id_history=idpatient).filter(appoint__range=(date1, date2))
    return render_to_response('cconline/medication_by_date.html',
        {
            'medications': medication,

        },
        context_instance=RequestContext(request)
    )