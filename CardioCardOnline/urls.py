# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.admin import UserChangeForm
from cconline.utils import ValidatingPasswordChangeForm


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'cconline.views.card_login'),
    url(r'^password_change/$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/accounts/password_change/done/',
         'password_change_form': ValidatingPasswordChangeForm},
        name="password_change"),
    url(r'^accounts/password_change/done/$',
        'django.contrib.auth.views.password_change_done'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^profile/$', 'cconline.views.profile', name='user_profile'),

    url(r'^$', 'cconline.views.index', name='index'),  # index page
    url(r'^stat/$', 'cconline.views.stat', name='stat'),  # stat page
    url(r'^search/', 'cconline.views.search', name='search'),  # search by num history or firstname patient
    url(r'^patients/my/', 'cconline.views.get_my_patient', name='my_patient'),  # my patients
    url(r'^patients/departs/(?P<iddepart>\d+)/$', 'cconline.views.patients_by_depart', name='departs_patient'),
    url(r'^patients/by_depart/', 'cconline.views.get_active_departs', name='patient_by_depart'),
    url(r'^patient/first_view/(?P<idpatient>\d+)/$', 'cconline.views.get_patient_first_view', name='patient_info'),
    url(r'^patient/cure/(?P<idpatient>\d+)/$', 'cconline.views.patient_cure', name='patient_cure'),
    url(r'^patient/(?P<idpatient>\d+)/$', 'cconline.views.get_patient', name='get_patient'),

    url(r'^diary/list/(?P<idpatient>\d+)/$', 'cconline.views.get_diary_list', name='list_diary'),
    url(r'^diary/(?P<id_diary>\d+)/$', 'cconline.views.get_diary', name='get_diary'),
    url(r'^diary/add/(?P<idpatient>\d+)/$', 'cconline.views.new_diary', name='add_diary'),
    url(r'^diary/save/$', 'cconline.views.save_diary', name='save_diary'),
    url(r'^diary/edit/(?P<id_diary>\d+)/$', 'cconline.views.edit_diary', name='edit_diary'),
    url(r'^diary/delete/(?P<id_diary>\d+)/$', 'cconline.views.delete_diary', name='delete_diary'),

    url(r'^examens/list/(?P<idpatient>\d+)/$', 'cconline.views.get_examen_list', name='list_exam'),
    url(r'^examen/(?P<id>\d+)/$', 'cconline.views.get_examen', name='get_exam'),
    url(r'^examen/add/(?P<idpatient>\d+)/$', 'cconline.views.add_new_exam', name='add_exam'),
    url(r'^examen/delete/(?P<id_exam>\d+)/$', 'cconline.views.delete_exam', name='delete_exam'),

    url(r'^laboratory/list/(?P<idpatient>\d+)/$', 'cconline.views.get_lab_list', name='list_lab'),
    url(r'^lab/add/(?P<idpatient>\d+)/$', 'cconline.views.add_new_laboratory', name='add_lab'),
    url(r'^labs/(?P<id>\d+)/$', 'cconline.views.get_laboratory', name='get_lab'),

    url(r'^operations/(?P<idpatient>\d+)/$', 'cconline.views.get_list_surgery', name='list_surgery'),
    url(r'^operation/(?P<id>\d+)/$', 'cconline.views.get_operation', name='operation'),

    url(r'^medication/list/(?P<idpatient>\d+)/$', 'cconline.views.get_list_medication', name='list_medication'),
    url(r'^medication/(?P<id>\d+)/$', 'cconline.views.get_medication', name='get_medication'),
    url(r'^prolong_medication/(?P<id>\d+)/$', 'cconline.views.prolong_medication', name='prolong_medication'),


    url(r'^proview/list/(?P<idpatient>\d+)/$', 'cconline.views.get_list_proffview', name='list_proview'),
    url(r'^proview/(?P<id>\d+)/$', 'cconline.views.get_proview', name='proview'),
    url(r'^proview/add/(?P<idpatient>\d+)/$', 'cconline.views.add_new_prof', name='add_prof'),
    url(r'^proview/save/$', 'cconline.views.save_prof', name='save_prof'),

    # nurse handler
    url(r'^nurse/work/$', 'cconline.nurse.get_nurse_work', name='nurse_work'),
    url(r'^nurse/list/(?P<idpatient>\d+)/$', 'cconline.nurse.get_nurse_list', name='list_nurse'),
    url(r'^temp_list/(?P<id>\d+)/$', 'cconline.nurse.get_tempearature_data', name='get_templist'),
    url(r'^risk_down/(?P<id>\d+)/$', 'cconline.nurse.get_risk_down', name='get_risk_down'),
    url(r'^pain_status/(?P<id>\d+)/$', 'cconline.nurse.get_pain_status', name='get_pain_status'),

    # post request urls
    url(r'^new_exam/', 'cconline.views.new_examen', name='save_exam'),
    url(r'^prolong_med/', 'cconline.views.prolong_med', name='save_prolong'),

    # utility for localnet
    url(r'^getpass/$', 'cconline.utils.getpass', name='get_password'),
    # url(r'^test/$', 'cconline.utils.gethttp'),
    url(r'^json/test/$', 'cconline.utils.json_test', name='get_test'),
    url(r'^json/subtest/$', 'cconline.utils.json_subtest', name='get_subtest'),
    url(r'^json/posttest/$', 'cconline.utils.json_savetest'),
    url(r'^json/templates/$', 'cconline.utils.json_templates', name='get_templates'),
    url(r'^json/nurse_work_lab/$', 'cconline.utils.json_nurse_lab', name='get_nurse_lab_work'),
    url(r'^json/nurse_work_med/$', 'cconline.utils.json_nurse_med', name='get_nurse_med_work'),
    url(r'^json/nurse_work_exam/$', 'cconline.utils.json_nurse_exam', name='get_nurse_exam_work'),
    url(r'^json/nurse_work_doc/$', 'cconline.utils.json_nurse_doctor', name='get_nurse_doctor_work'),
    url(r'^json/nurse_execute/$', 'cconline.utils.nurse_execute', name='get_nurse_execute'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

# server error pages handlers
handler404 = 'cconline.utils.page_not_found'
handler403 = 'cconline.utils.permission_denied'
handler500 = 'cconline.utils.server_error'
