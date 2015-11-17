from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cconline.views.index',  name='index'),#index page
    url(r'^patients/my/', 'cconline.views.get_my_patient', name='my_patient'),
    url(r'^patients/departs/(?P<iddepart>\d+)/$', 'cconline.views.patients_by_depart', name='departs_patient'),
    url(r'^patients/by_depart/', 'cconline.views.get_active_departs', name='active_departs'),
    url(r'patient/getinfo/(?P<idpatient>\d+)/$', 'cconline.views.get_patient_info', name='patinet_info'),
    url(r'^patient/(?P<idpatient>\d+)/$', 'cconline.views.get_patient', name='get_patient'),
    url(r'^diary/list/(?P<idpatient>\d+)/$', 'cconline.views.get_diary_list', name='list_diary'),
    url(r'^diary/(?P<id>\d+)/$', 'cconline.views.get_diary', name='get_diary'),
    url(r'^examens/list/(?P<idpatient>\d+)/$', 'cconline.views.get_examen_list', name='list_exam'),
    url(r'^examen/(?P<id>\d+)/$', 'cconline.views.get_examen', name='get_exam'),
    url(r'^laboratory/list/(?P<idpatient>\d+)/$', 'cconline.views.get_lab_list', name='list_lab'),
    url(r'^labs/(?P<id>\d+)/$', 'cconline.views.get_laboratory', name='get_lab'),
    url(r'^temp_list/(?P<id>\d+)/$', 'cconline.views.get_tempearature_data', name='get_templist'),
    url(r'^risk_down/(?P<id>\d+)/$', 'cconline.views.get_risk_down', name='get_risk_down'),
    url(r'^pain_status/(?P<id>\d+)/$', 'cconline.views.get_pain_status', name='get_pain_status'),


#    url(r'^medication/list/(?P<idpatient>\d+)/$', 'cconline.views.get_my_patient', name='my_patient'),
#    url(r'^proffview/list/(?P<idpatient>\d+)/$', 'cconline.views.get_my_patient', name='my_patient'),
    url(r'^nurse/list/(?P<idpatient>\d+)/$', 'cconline.views.get_nurse_list', name='list_nurse'),
]
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()