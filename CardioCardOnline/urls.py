# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin, auth
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import password_change, password_change_done, logout
from cconline.utils import ValidatingPasswordChangeForm
from cconline import views
from cconline import nurse
from cconline import utils


admin.autodiscover()

urlpatterns = [
    url(r'^robots.txt$', views.robots),
    url(r'^login/$', views.card_login),
    url(r'^password_change/$',
        password_change,
        {'post_change_redirect': '/accounts/password_change/done/',
         'password_change_form': ValidatingPasswordChangeForm},
        name="password_change"),
    url(r'^accounts/password_change/done/$',
        password_change_done),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^profile/$', views.profile, name='user_profile'),

    url(r'^$', views.index, name='index'),  # index page
    url(r'^stat/$', views.stat, name='stat'),  # stat page
    url(r'^search/', views.search, name='search'),  # search by num history or firstname patient
    url(r'^about/', views.about, name='about'),  # search by num history or firstname patient
    url(r'^map/', views.patient_map, name='patient_map'),
    url(r'^last_test/', views.choose_test, name='choose_test'), # choose test lab or exam
    url(r'^last_lab/(?P<iddepart>\d+)/$', views.last_lab, name='last_laboratory'), # last lab
    url(r'^last_exam/(?P<iddepart>\d+)/$', views.last_exam, name='last_examenation'), # last exam
    url(r'^patients/my/', views.get_my_patient, name='my_patient'),  # my patients
    url(r'^patients/monpat/', views.get_mon_patients, name='under_observation'),  # patients under_observation
    url(r'^patients/departs/(?P<iddepart>\d+)/$', views.patients_by_depart, name='departs_patient'),
    url(r'^patients/by_depart/', views.get_active_departs, name='patient_by_depart'),
    url(r'^patient/first_view/(?P<idpatient>\d+)/$', views.get_patient_first_view, name='patient_info'),
    url(r'^patient/cure/(?P<idpatient>\d+)/$', views.patient_cure, name='patient_cure'),
    url(r'^patient/(?P<idpatient>\d+)/$', views.get_patient, name='get_patient'),
    url(r'^patient/editview/(?P<idpatient>\d+)/(?P<idparam>\d+)/$', views.get_doctor_view, name='get_doctor_view'),
    url(r'^patient/addview/(?P<idpatient>\d+)/$', views.add_doctor_view, name='add_doctor_view'),
    url(r'^patient/view/save/$', views.save_doctor_view, name='save_doctor_view'),

    url(r'^diary/list/(?P<idpatient>\d+)/$', views.get_diary_list, name='list_diary'),
    url(r'^diary/(?P<id_diary>\d+)/$', views.get_diary, name='get_diary'),
    url(r'^diary/add/(?P<idpatient>\d+)/$', views.new_diary, name='add_diary'),
    url(r'^diary/save/$', views.save_diary, name='save_diary'),
    url(r'^diary/edit/(?P<id_diary>\d+)/$', views.edit_diary, name='edit_diary'),
    url(r'^diary/delete/(?P<id_diary>\d+)/$', views.delete_diary, name='delete_diary'),

    url(r'^examens/list/(?P<idpatient>\d+)/$', views.get_examen_list, name='list_exam'),
    url(r'^examen/(?P<id>\d+)/$', views.get_examen, name='get_exam'),
    url(r'^examen/add/(?P<idpatient>\d+)/$', views.add_new_exam, name='add_exam'),
    url(r'^examen/delete/(?P<id_exam>\d+)/$', views.delete_exam, name='delete_exam'),

    url(r'^laboratory/list/(?P<idpatient>\d+)/$', views.get_lab_list, name='list_lab'),
    url(r'^lab/add/(?P<idpatient>\d+)/$', views.add_new_laboratory, name='add_lab'),
    url(r'^labs/(?P<id>\d+)/$', views.get_laboratory, name='get_lab'),

    url(r'^operations/(?P<idpatient>\d+)/$', views.get_list_surgery, name='list_surgery'),
    url(r'^operation/(?P<id>\d+)/$', views.get_operation, name='operation'),

    url(r'^medication/list/(?P<idpatient>\d+)/$', views.get_list_medication, name='list_medication'),
    url(r'^medication/list_by_date/(?P<idpatient>\d+)/$', views.get_list_medication_by_date, name='list_medication_by_date'),
    url(r'^medication/bydate/(?P<idpatient>\d+)/(?P<date_assign>[\w\-]+)/$', views.get_medication_by_date, name='medication_by_date'),
    url(r'^medication/(?P<id>\d+)/$', views.get_medication, name='get_medication'),
    url(r'^prolong_medication/(?P<id>\d+)/$', views.prolong_medication, name='prolong_medication'),


    url(r'^proview/list/(?P<idpatient>\d+)/$', views.get_list_proffview, name='list_proview'),
    url(r'^proview/(?P<id>\d+)/$', views.get_proview, name='proview'),
    url(r'^proview/add/(?P<idpatient>\d+)/$', views.add_new_prof, name='add_prof'),
    url(r'^proview/save/$', views.save_prof, name='save_prof'),
    url(r'^proview/edit/(?P<id>\d+)$', views.edit_prof_conclusion, name='edit_prof'),
    url(r'^proview/save_pv/$', views.save_prof_conclusion, name='save_prof_conclusion'),

    # nurse handler
    url(r'^nurse/work/$', nurse.get_nurse_work, name='nurse_work'),
    url(r'^nurse/list/(?P<idpatient>\d+)/$', nurse.get_nurse_list, name='list_nurse'),
    url(r'^temp_list/(?P<id>\d+)/$', nurse.get_tempearature_data, name='get_temperature_list'),
    url(r'^risk_down/(?P<id>\d+)/$', nurse.get_risk_down, name='get_risk_down'),
    url(r'^pain_status/(?P<id>\d+)/$', nurse.get_pain_status, name='get_pain_status'),
    url(r'^nurse_view/(?P<id>\d+)/$', nurse.get_nurse_view, name='get_nurse_view'),
    url(r'^nurse/patients/$', nurse.get_nurse_patients, name='nurse_patients'),
    url(r'^nurse/patient/(?P<id>\d+)/$', nurse.get_nurse_patient, name='nurse_patient'),

    # post request urls
    url(r'^new_exam/', views.new_examen, name='save_exam'),
    url(r'^prolong_med/', views.prolong_med, name='save_prolong'),

    # utility for localnet
    url(r'^getpass/$', utils.getpass, name='get_password'),
    url(r'^json/test/$', utils.json_test, name='get_test'),
    url(r'^json/subtest/$', utils.json_subtest, name='get_subtest'),
    url(r'^json/posttest/$', utils.json_savetest),
    url(r'^json/templates/$', utils.json_templates, name='get_templates'),
    url(r'^json/nurse_work_lab/$', utils.json_nurse_lab, name='get_nurse_lab_work'),
    url(r'^json/nurse_work_med/$', utils.json_nurse_med, name='get_nurse_med_work'),
    url(r'^json/nurse_work_exam/$', utils.json_nurse_exam, name='get_nurse_exam_work'),
    url(r'^json/nurse_work_doc/$', utils.json_nurse_doctor, name='get_nurse_doctor_work'),
    url(r'^json/nurse_execute/$', utils.nurse_execute, name='get_nurse_execute'),
    url(r'^json/nurse/$', utils.nurse_work_by_patient, name='get_nurse_json'),
    url(r'^get_map/$', views.patient_map_json)
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# server error pages handlers
handler404 = utils.page_not_found
handler403 = utils.permission_denied
handler500 = utils.server_error
