from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',  'cconline.views.card_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    url(r'^$', 'cconline.views.index',  name='index'),#index page
    url(r'^search/', 'cconline.views.search', name='search'),#search by num history or firstname patient
    url(r'^patients/my/', 'cconline.views.get_my_patient', name='my_patient'),#my patients
    url(r'^patients/departs/(?P<iddepart>\d+)/$', 'cconline.views.patients_by_depart', name='departs_patient'),
    url(r'^patients/by_depart/', 'cconline.views.get_active_departs', name='active_departs'),
    url(r'^patient/first_view/(?P<idpatient>\d+)/$', 'cconline.views.get_patient_first_view', name='patient_info'),
    url(r'^patient/(?P<idpatient>\d+)/$', 'cconline.views.get_patient', name='get_patient'),
    url(r'^diary/list/(?P<idpatient>\d+)/$', 'cconline.views.get_diary_list', name='list_diary'),
    url(r'^diary/(?P<id>\d+)/$', 'cconline.views.get_diary', name='get_diary'),
    url(r'^examens/list/(?P<idpatient>\d+)/$', 'cconline.views.get_examen_list', name='list_exam'),
    url(r'^examen/(?P<id>\d+)/$', 'cconline.views.get_examen', name='get_exam'),
    url(r'^examen/add/(?P<idpatient>\d+)/$', 'cconline.views.add_new_exam', name='add_exam'),
    url(r'^laboratory/list/(?P<idpatient>\d+)/$', 'cconline.views.get_lab_list', name='list_lab'),
    url(r'^labs/(?P<id>\d+)/$', 'cconline.views.get_laboratory', name='get_lab'),
    url(r'^nurse/list/(?P<idpatient>\d+)/$', 'cconline.views.get_nurse_list', name='list_nurse'),
    url(r'^temp_list/(?P<id>\d+)/$', 'cconline.views.get_tempearature_data', name='get_templist'),
    url(r'^risk_down/(?P<id>\d+)/$', 'cconline.views.get_risk_down', name='get_risk_down'),
    url(r'^pain_status/(?P<id>\d+)/$', 'cconline.views.get_pain_status', name='get_pain_status'),
    url(r'^operations/(?P<idpatient>\d+)/$', 'cconline.views.get_list_surgery', name='list_surgery'),
    url(r'^operation/(?P<id>\d+)/$', 'cconline.views.get_operation', name='operation'),
    url(r'^medication/list/(?P<idpatient>\d+)/$', 'cconline.views.get_list_medication', name='list_medication'),
    url(r'^medication/(?P<id>\d+)/$', 'cconline.views.get_medication', name='medication'),
    url(r'^proview/list/(?P<idpatient>\d+)/$', 'cconline.views.get_list_proffview', name='proview'),
    url(r'^proview/(?P<id>\d+)/$', 'cconline.views.get_proview', name='proview'),
    url(r'^prolong_medication/(?P<id>\d+)/$', 'cconline.views.prolong_medication', name='prolong_medication'),

    #post request urls
    url(r'^new_exam/', 'cconline.views.new_examen', name='save_exam'),
    url(r'^prolong_med/', 'cconline.views.prolong_med', name='save_prolong'),



    #utility for localnet
    url(r'^getpass/$', 'cconline.utils.getpass', name='get_password'),
    #url(r'^test/$', 'cconline.utils.gethttp'),
]
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()

#server error pages handlers
handler404 = 'cconline.utils.page_not_found'
handler403 = 'cconline.utils.permission_denied'
handler500 = 'cconline.utils.server_error'