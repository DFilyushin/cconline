# -*- coding: utf-8 -*-
from _ast import mod

from django.db import models
from django.db import connection
from django.contrib.auth.signals import user_logged_in
from collections import namedtuple
# Database model


class Departments(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'departments'


class Personal(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, db_column='DOCNAME')
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')
    honor = models.CharField(max_length=1021, db_column='HONORS')
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')

    class Meta:
        managed = False
        db_table = 'VW_REF_MEDPROFF'


class ClassMkb(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    parent_id = models.IntegerField(db_column='PARENT_ID', blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=1020, blank=True)
    code = models.CharField(db_column='CODE', max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = 'class_mkb'


class RefSocial(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True)
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True)
    last_user = models.CharField(db_column='LAST_USER', max_length=320, blank=True)
    last_date = models.DateTimeField(db_column='LAST_DATE', blank=True, null=True)
    name = models.CharField(db_column='NAME', unique=True, max_length=1020)
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ref_social'


class ListSpecialization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(db_column='NAME', max_length=255)

    class Meta:
        managed = False
        db_table = 'VW_REF_SPECILIZATION'


class RefNationality(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    name_rus = models.CharField(db_column='NAME_RUS', unique=True, max_length=1020)
    name_kaz = models.CharField(db_column='NAME_KAZ', max_length=1020)
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True)
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True)
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True)

    class Meta:
        managed = False
        db_table = 'ref_nationality'


class RefBenefit(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True)
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True)
    name = models.CharField(db_column='NAME', unique=True, max_length=1020)
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ref_benefit'


class RefCity(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    id_parent = models.IntegerField(db_column='ID_PARENT', blank=True, null=True)
    k = models.IntegerField(db_column='K', blank=True, null=True)
    name_rus = models.CharField(db_column='NAME_RUS', max_length=1020, blank=True)
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True)
    is_city = models.SmallIntegerField(db_column='IS_CITY', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ref_city'


class History(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True)
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True)
    last_date = models.DateTimeField(db_column='LAST_DATE', blank=True, null=True)
    last_user = models.CharField(db_column='LAST_USER', max_length=320, blank=True)
    lastname = models.CharField(db_column='LASTNAME', max_length=1020, blank=True)
    firstname = models.CharField(db_column='FIRSTNAME', max_length=1020, blank=True)
    middlename = models.CharField(db_column='MIDDLENAME', max_length=1020, blank=True)
    dob = models.DateField(db_column='DOB', blank=True, null=True)
    gender = models.SmallIntegerField(db_column='GENDER', blank=True, null=True)
    iin = models.CharField(db_column='IIN', max_length=48, blank=True)
    bar_code = models.CharField(db_column='BAR_CODE', max_length=48, blank=True)
    live_address = models.CharField(db_column='LIVE_ADDRESS', max_length=1020, blank=True)
    insurence_company = models.CharField(db_column='INSURENCE_COMPANY', max_length=1020, blank=True)
    insurence_number = models.CharField(db_column='INSURENCE_NUMBER', max_length=100, blank=True)
    med_reg_number = models.CharField(db_column='MED_REG_NUMBER', max_length=100, blank=True)
    id_social = models.ForeignKey('RefSocial', db_column='ID_SOCIAL', blank=True, null=True)
    id_nationality = models.ForeignKey('RefNationality', db_column='ID_NATIONALITY', blank=True, null=True)
    id_benefit = models.ForeignKey('RefBenefit', db_column='ID_BENEFIT', blank=True, null=True)
    id_city = models.ForeignKey('RefCity', db_column='ID_CITY', blank=True, null=True)
    workplace = models.CharField(db_column='WORKPLACE', max_length=2048, blank=True)
    study = models.CharField(db_column='STUDY', max_length=2048, blank=True)
    num_history = models.CharField(db_column='NUM_HISTORY', max_length=100, blank=True)
    receipt = models.DateTimeField(db_column='RECEIPT', blank=True, null=True)
    extreme_type = models.SmallIntegerField(db_column='EXTREME_TYPE', blank=True, null=True)
    id_type_hospitalize = models.IntegerField(db_column='ID_TYPE_HOSPITALIZE', blank=True, null=True)
    id_depart = models.ForeignKey(Departments, db_column='ID_DEPART', blank=True, null=True)
    id_doctor = models.ForeignKey(Personal, db_column='id_doctor', blank=False, null=False)
    chamber = models.CharField(db_column='CHAMBER', max_length=1020, blank=True)
    incoming_diag = models.CharField(db_column='INCOMING_DIAG', max_length=4096, blank=True)
    id_clinic_diag = models.ForeignKey(ClassMkb, db_column='ID_CLINIC_DIAG', blank=True, null=True, related_name='+')
    id_lpu_diag = models.ForeignKey(ClassMkb, db_column='ID_LPU_DIAG', blank=True, null=True)
    diag_lpu = models.CharField(db_column='DIAG_LPU', max_length=4096, blank=True)
    id_related_diag = models.ForeignKey(ClassMkb, db_column='ID_RELATED_DIAG', blank=True, null=True, related_name='+')
    related_diagnosis = models.CharField(db_column='RELATED_DIAGNOSIS', max_length=4096, blank=True)
    id_main_diag = models.IntegerField(db_column='ID_MAIN_DIAG', blank=True, null=True)
    id_compl_diag = models.IntegerField(db_column='ID_COMPL_DIAG', blank=True, null=True)
    id_end_diag = models.IntegerField(db_column='ID_END_DIAG', blank=True, null=True)
    id_from = models.IntegerField()
    type_warior = models.IntegerField(db_column='TYPE_WARIOR', blank=True, null=True)
    discharge = models.DateTimeField(db_column='DISCHARGE', blank=True, null=True) 
    id_cancer_treatment = models.IntegerField()
    baby_massa = models.DecimalField(db_column='BABY_MASSA', max_digits=15, decimal_places=2, blank=True, null=True)
    baby_length = models.DecimalField(db_column='BABY_LENGTH', max_digits=15, decimal_places=2, blank=True, null=True)
    hosp_with_mother = models.SmallIntegerField(db_column='HOSP_WITH_MOTHER', blank=True, null=True)
    hosp_hour_after_disease = models.IntegerField(db_column='HOSP_HOUR_AFTER_DISEASE', blank=True, null=True)
    id_result = models.IntegerField()
    id_treatment_effect = models.IntegerField(db_column='ID_TREATMENT_EFFECT', blank=True, null=True)
    main_diag = models.CharField(db_column='MAIN_DIAG', max_length=4096, blank=True)
    main_complication = models.CharField(db_column='MAIN_COMPLICATION', max_length=4096, blank=True)
    send_to = models.CharField(db_column='SEND_TO', max_length=1020, blank=True)
    date_set_diag = models.DateTimeField(db_column='DATE_SET_DIAG', blank=True, null=True)
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True)
    id_lpu = models.IntegerField()
    archive_send = models.DateField(db_column='ARCHIVE_SEND', blank=True, null=True)
    is_signed = models.SmallIntegerField(db_column='IS_SIGNED', blank=True, null=True)
    who_signed = models.CharField(db_column='WHO_SIGNED', max_length=320, blank=True)
    id_bedregime = models.IntegerField()
    clinic_diag = models.CharField(db_column='CLINIC_DIAG', max_length=4096, blank=True)
    type_card = models.IntegerField(db_column='TYPE_CARD', blank=True, null=True)
    viral_diseases = models.CharField(db_column='VIRAL_DISEASES', max_length=2048, blank=True)
    chronic_diseases = models.CharField(db_column='CHRONIC_DISEASES', max_length=2048, blank=True)
    preliminary_diag = models.CharField(db_column='PRELIMINARY_DIAG', max_length=4096, blank=True)
    drug_intolerance = models.CharField(db_column='DRUG_INTOLERANCE', max_length=2048, blank=True)
    id_typepay = models.IntegerField()
    date_first_view = models.DateTimeField(db_column='DATE_FIRST_VIEW', blank=True, null=True)
    id_finance = models.IntegerField()
    id_ext_doctor_view = models.IntegerField(db_column='ID_EXT_DOCTOR_VIEW', blank=True, null=True)
    date_first_view_ext = models.DateTimeField(db_column='DATE_FIRST_VIEW_EXT', blank=True, null=True)
    id_initnurse = models.IntegerField(db_column='ID_INITNURSE', blank=True, null=True)
    is_view = models.SmallIntegerField(db_column='IS_VIEW', blank=True, null=True)
    go_cardiosurgery = models.DateTimeField(db_column='GO_CARDIOSURGERY', blank=True, null=True)
    go_reahab = models.DateTimeField(db_column='GO_REAHAB', blank=True, null=True)
    id_bedtype = models.IntegerField(db_column='ID_BEDTYPE', blank=True, null=True)
    type_trauma = models.SmallIntegerField(db_column='TYPE_TRAUMA', blank=True, null=True)
    id_patient_sender = models.IntegerField(db_column='ID_PATIENT_SENDER', blank=True, null=True)
    type_hospit = models.SmallIntegerField(db_column='TYPE_HOSPIT', blank=True, null=True)
    count_hospit_inyear = models.SmallIntegerField(db_column='COUNT_HOSPIT_INYEAR', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history'

    def get_blood_type(self, idHistory):
        # Get patient blood type
        cursor = connection.cursor()
        sql = 'SELECT TYPE_BLOOD FROM SP_GET_TYPE_BLOOD (%s)' % idHistory
        cursor.execute(sql)
        row = cursor.fetchone()
        return row[0]

    def get_age(self):
        # Age of patient
        d1 = self.dob.strftime("%Y-%m-%d")
        d2 = self.receipt.strftime("%Y-%m-%d")
        cursor = connection.cursor()
        sql = "select (Datediff(month, cast('%s' as date), cast('%s' as date)) / 12) from rdb$database" % (d1, d2)
        cursor.execute(sql)
        row = cursor.fetchone()
        return row[0]


class ListHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    num_history = models.CharField(max_length=25)
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)
    depart_name = models.CharField(max_length=255)
    dob = models.DateField()
    yearof = models.IntegerField()
    receipt = models.DateTimeField()
    discharge = models.DateTimeField()
    id_doctor = models.IntegerField()
    id_depart = models.IntegerField()
    doctor = models.CharField(max_length=255, db_column='DOCTOR_NAME')

    class Meta:
        managed = False
        db_table = 'VW_HISTORY'


class ListDiary(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_department = models.IntegerField()
    id_doctor = models.IntegerField()
    reg_date = models.DateTimeField()
    doctor = models.CharField(max_length=255)
    depart_name = models.CharField(max_length=255)
    diary_name = models.CharField(max_length=255, db_column='DIARY_NAME')
    blob_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'VW_DIARY'


class ListAnalysis(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_doctor = models.IntegerField()
    id_labanalysis = models.CharField(max_length=10)
    date_assign = models.DateTimeField(db_column='DATE_ASSIGN', blank=True, null=True)
    date_plan = models.DateTimeField(db_column='DATE_PLAN', blank=True, null=True)
    id_executer = models.IntegerField(db_column='ID_EXECUTER', blank=True, null=True)
    date_execute = models.DateTimeField(db_column='DATE_EXECUTE', blank=True, null=True)
    id_nurse_execute = models.IntegerField(db_column='ID_NURSE_EXECUTE', blank=True, null=True)
    nurse_date_execute = models.DateTimeField(db_column='NURSE_DATE_EXECUTE', blank=True, null=True)
    id_med_cancel = models.IntegerField(db_column='ID_MED_CANCEL', blank=True, null=True)
    cancel_cause = models.CharField(db_column='CANCEL_CAUSE', max_length=1020, blank=True)
    is_cito = models.SmallIntegerField(db_column='IS_CITO', blank=True, null=True)
    lab_comment = models.CharField(db_column='LAB_COMMENT', max_length=4096, blank=True)
    name_labanalysis = models.CharField(db_column='NAME_LABANALYSIS', max_length=255)
    doctor = models.CharField(max_length=255)
    depart = models.CharField(db_column='DEPARTMENT', max_length=255)

    class Meta:
        managed = False
        db_table = 'VW_ASSIGNED_ANALYSIS'


class LaboratoryData(models.Model):
    id = models.IntegerField(primary_key=True)
    id_assigned_anal = models.IntegerField()
    ad_value = models.CharField(max_length=7168)
    measure = models.CharField(max_length=10)
    norm_value = models.CharField(max_length=255)
    param_name = models.CharField(db_column='name', max_length=255)
    sort_pos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'VW_LABORATORY_DATA'


class ActiveDepart(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    cnt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'VW_ACTIVE_DEPART'


class ListExamens(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_doctor = models.IntegerField()
    id_executer = models.IntegerField()
    date_assign = models.DateTimeField(db_column='APPOINTMENT_DATE')
    date_plan = models.DateTimeField(db_column='PLAN_DATE')
    date_nurse = models.DateTimeField(db_column='NURSE_DATE_EXECUTE')
    date_execute = models.DateTimeField(db_column='DATETIME_EXECUTE')
    name_exam = models.CharField(max_length=255, db_column='GROUP_NAME')
    doctor = models.CharField(max_length=255, db_column='APPOINT_DOCTOR')
    doctor_executer = models.CharField(max_length=255, db_column='EXECUTER_DOCTOR')
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')
    patient = models.CharField(max_length=3064)
    num_history = models.CharField(max_length=25)
    feature_data = models.TextField(db_column='features')
    conclusion = models.TextField(db_column='conclusion')

    class Meta:
        managed = False
        db_table = 'VW_ASSIGNED_EXAMENATION'


class TemperatureList(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_nurse = models.IntegerField()
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')
    date_view = models.DateTimeField(db_column='DATE_CTRL')
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')
    nurse = models.CharField(max_length=255)
    patient = models.CharField(max_length=3068)
    num_card = models.CharField(max_length=25)
    id_group = models.IntegerField(db_column='GROUP_PARAM')

    class Meta:
        managed = False
        db_table = 'VW_NURSE_CTRL_PARAM'


class NurseViewList(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_nurse = models.IntegerField()
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')
    date_view = models.DateTimeField(db_column='DATE_INSPECT')
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')
    nurse = models.CharField(max_length=255)
    patient = models.CharField(max_length=3068)
    num_card = models.CharField(max_length=25, db_column='NUM_HISTORY')

    class Meta:
        managed = False
        db_table = 'VW_INSPECTION_NURSE'


class RiskDownList(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_nurse = models.IntegerField()
    id_depart = models.IntegerField()
    date_view = models.DateTimeField(db_column='rd_datetime')
    depart = models.CharField(max_length=255, db_column='department')
    nurse = models.CharField(max_length=255, db_column='docname')
    patient = models.CharField(max_length=3068, db_column='FIO')
    num_card = models.CharField(max_length=25, db_column='num_history')

    class Meta:
        managed = False
        db_table = 'VW_RISKDOWN_STATUS'


class PainStatusList(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_nurse = models.IntegerField()
    id_depart = models.IntegerField()
    date_view = models.DateTimeField(db_column='PS_DATETIME')
    depart = models.CharField(max_length=255, db_column='department')
    nurse = models.CharField(max_length=255)
    patient = models.CharField(max_length=3068, db_column='PATIENT_FIO')
    num_card = models.CharField(max_length=25, db_column='NUM_HISTORY')

    class Meta:
        managed = False
        db_table = 'VW_PAIN_STATUS'


class TemperatureData(models.Model):
    id = models.IntegerField(primary_key=True)
    id_ctrl_nurse = models.IntegerField()
    param_name = models.CharField(max_length=255)
    value1 = models.FloatField()
    value2 = models.FloatField()
    unit = models.CharField(max_length=50)
    sort_pos = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'VW_TEMPLISTDATA'


class RiskDownData(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_nurse = models.IntegerField()
    id_depart = models.IntegerField()
    patient = models.CharField(max_length=3068, db_column='FIO')
    num_history = models.CharField(max_length=25)
    date_view = models.DateTimeField(db_column='RD_DATETIME')
    is_down_three_month = models.IntegerField(db_column='IS_DOWN3MONTH')
    is_assoc_desease = models.IntegerField(db_column='IS_ASSOC_DISEASE')
    type_walk = models.IntegerField()
    is_take_medicament = models.IntegerField()
    type_gait = models.IntegerField()
    what_make = models.CharField(max_length=255)
    depart = models.CharField(max_length=255, db_column='department')
    nurse = models.CharField(max_length=255, db_column='docname')
    is_norm_psi = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'VW_RISKDOWN_STATUS'


class PainStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_nurse = models.IntegerField()
    id_depart = models.IntegerField()
    patient = models.CharField(max_length=3068, db_column='PATIENT_FIO')
    num_history = models.CharField(max_length=25)
    date_view = models.DateTimeField(db_column='PS_DATETIME')
    pain_value = models.IntegerField()
    id_type_pain = models.IntegerField()
    id_care = models.IntegerField()
    pain_place = models.CharField(max_length=1024)
    is_allergy = models.SmallIntegerField(db_column='se_allergy')
    is_adaptation = models.SmallIntegerField(db_column='se_adaptation')
    is_puke = models.SmallIntegerField(db_column='se_puke')
    is_latch = models.SmallIntegerField(db_column='se_latch')
    is_pain_inside = models.SmallIntegerField(db_column='SE_PAININSIDE')
    is_other = models.CharField(max_length=255, db_column='se_other')
    nurse = models.CharField(max_length=255)
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')
    type_pain_str = models.CharField(max_length=255, db_column='TYPE_PAIN_STR')
    type_care = models.CharField(max_length=255, db_column='TYPE_CARE')

    class Meta:
        managed = False
        db_table = 'VW_PAIN_STATUS'


class PatientInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_param = models.IntegerField()
    id_view = models.IntegerField(db_column='ID_DOCTORVIEW')
    param_name = models.CharField(max_length=255, db_column='NAME')
    text = models.TextField(db_column='VAL_TEXT')

    class Meta:
        managed = False
        db_table = 'VW_DATA_BLOB'

    @staticmethod
    def check_uniq_param(id_history, id_param):
        #
        # Проверяет уникальность записи осмотра, для исключения двойного описания состояния
        # True - уникальна запись, добавлять можно, False - неуникальна
        cursor = connection.cursor()
        sql = "select count(*) from data_blob where id_history = %s and id_doctorview = 0 and id_param = %s" % \
              (id_history, id_param)
        cursor.execute(sql)
        row = cursor.fetchone()
        return row[0] == 0

    @staticmethod
    def get_non_existent_view(id_history):
        #
        # Список записей осмотров, которых у пациента ещё нет
        #
        cursor = connection.cursor()
        sql = "select id_param, page_name from page_group where group_name = 'AMBULANCE'" \
              "and not exists (select id from data_blob db where db.id_history = %s " \
              "and db.id_doctorview = 0 and db.id_param = page_group.id_param)" % id_history
        cursor.execute(sql)
        # "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class ListSurgery(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    num_history = models.CharField(max_length=25)
    patient = models.CharField(max_length=3068, db_column='FIO')
    num_protokol = models.CharField(max_length=25)
    surgery_date = models.DateField(db_column='OPER_START')
    surgery_type = models.CharField(max_length=24, db_column='TYPE_OPER_NAME')
    surgery_name = models.CharField(max_length=4308, db_column='OPER_NAME')
    surgery_extreme = models.SmallIntegerField(db_column='EXTREME_TYPE')
    conclusion = models.TextField(db_column='CONCLUSION')
    type_operation = models.IntegerField(db_column='TYPE_OPER')

    class Meta:
        managed = False
        db_table = 'VW_SURGERY'


class SurgeryAdv(models.Model):
    id = models.IntegerField(primary_key=True)
    id_surgery = models.IntegerField(db_column='ID_SURGERY')
    id_type = models.IntegerField(db_column='ID_ATTRIBUT')
    text_value = models.TextField(db_column='STR_VALUE')

    class Meta:
        managed = False
        db_table = 'SURGERY_ATTRVAL'


class ListProffView(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    specname = models.CharField(max_length=255, db_column='SPECIALIZATION')
    num_history = models.CharField(max_length=25)
    patient = models.CharField(max_length=3068)
    assigndate = models.DateTimeField(db_column='DATE_ASSIGN')
    viewdate = models.DateTimeField(db_column='DATE_VIEW')
    doctor = models.CharField(max_length=255, db_column='DOCTOR')
    conclusion = models.TextField(db_column='CONCLUSION')

    class Meta:
        managed = False
        db_table = 'VW_PROF_DOCTOR_VIEW'


class HistoryMedication(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_key_record')
    id_history = models.IntegerField()
    medic_name = models.CharField(max_length=1020, db_column='medic_name')

    class Meta:
        managed = False
        db_table = 'VW_HISTORY_MEDICATION'
        ordering = ['medic_name']


class Medication(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_key = models.IntegerField(db_column='ID_KEY_RECORD')
    id_department = models.IntegerField()
    appl_form = models.CharField(max_length=255, db_column='APPL_FORM_NAME')
    form = models.CharField(max_length=10)
    composit = models.CharField(max_length=512, db_column='DRUG_COMPOSIT')
    doctor = models.CharField(max_length=255)
    speed_inj = models.CharField(max_length=50, db_column='SPEED_IN')
    count_drug = models.FloatField(db_column='CNT_DRUG')
    dose = models.CharField(max_length=255, db_column='DOSE')
    appoint = models.DateTimeField(db_column='START_APPOINTMENT')
    eat_time = models.DateTimeField(db_column='DATETIME_EAT')
    medic_name = models.CharField(max_length=255, db_column='MEDICAMENT_NAME')

    class Meta:
        managed = False
        db_table = 'VW_ASSIGNED_MEDICATION'
        ordering = ['appoint']


class SysUsers(models.Model):
    user_login = models.CharField(primary_key=True, max_length=25)
    id_doctor = models.IntegerField()
    user_fullname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'SYS_USERS'


class UserGroups(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    sys_login = models.CharField(max_length=80)
    sys_group = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'VW_USER_IN_GROUP'


class RefExamens(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, db_column='NAME_GROUP')

    class Meta:
        managed = False
        db_table = 'VW_REF_EXAM_GROUP'


class ExamenDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField(null=False)
    id_doctor = models.IntegerField(null=False)
    id_department = models.IntegerField(null=False)
    id_group_examenation = models.IntegerField(null=False)
    appointment_date = models.DateTimeField(null=False)
    plan_date = models.DateTimeField(null=False)
    id_typepay = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = 'ASSIGNED_EXAMENATION'


class ListOfAnalysis(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'VW_MASTER_ANALYSIS'


class ListAllAnalysis(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    id_parent = models.CharField(max_length=10)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'VW_ALL_ANALYSIS'


class ExamParam(models.Model):
    id = models.IntegerField(primary_key=True, db_column='UN_ID')
    param = models.CharField(max_length=255, db_column='PARAM_NAME')
    type = models.IntegerField(db_column='PARAM_TYPE')
    measure = models.CharField(max_length=40, db_column='PARAM_MEASURE')
    value = models.CharField(max_length=7168, db_column='PARAM_VALUE')


class Diary(models.Model):
    id = models.AutoField(primary_key=True)
    id_history = models.IntegerField()
    diary_name = models.CharField(max_length=255, db_column='DIARY_NAME', blank=True)
    diary_date = models.DateTimeField(db_column='REG_DATE')
    id_doctor = models.IntegerField()
    doctor = models.CharField(max_length=255, db_column='DOCTOR')
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')
    depart = models.CharField(max_length=255, db_column='DEPART_NAME')
    diary_text = models.TextField(db_column='BLOB_TEXT')

    class Meta:
        managed = False
        db_table = 'VW_DIARY'


class Templates(models.Model):
    id = models.IntegerField(primary_key=True)
    id_template = models.IntegerField()
    id_type = models.IntegerField(db_column='TYPE_TEMPLATE')
    name = models.CharField(max_length=255, db_column='TEMPL_NAME')
    text = models.TextField(db_column='text_blob')

    class Meta:
        managed = False
        db_table = 'TEMPLATES'


class ListTemplates(models.Model):
    id = models.IntegerField(primary_key=True)
    id_template = models.IntegerField()
    id_type = models.IntegerField(db_column='TYPE_TEMPLATE')
    name = models.CharField(max_length=255, db_column='TEMPL_NAME')

    class Meta:
        managed = False
        db_table = 'TEMPLATES'


class ProfDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    id_history = models.IntegerField()
    id_spec = models.IntegerField(db_column='ID_SPECIALIZATION')
    assign_date = models.DateTimeField(db_column='DATE_ASSIGN')
    plan_date = models.DateTimeField(db_column='PLAN_DATE')
    id_doctor = models.IntegerField(db_column='ID_ASSIGN_DOCTOR')
    id_depart = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'PROF_DOCTOR_VIEW'


class NurseLabWork(models.Model):
    id = models.IntegerField(primary_key=True)
    num_history = models.CharField(max_length=25)
    doctor = models.CharField(max_length=255)
    patient = models.CharField(max_length=3064, db_column='PATIENT')
    analysis = models.CharField(max_length=255, db_column='NAME_LABANALYSIS')
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')
    datetime_plan = models.DateTimeField(db_column='DATE_PLAN')
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')
    is_cito = models.SmallIntegerField(db_column='IS_CITO')
    date_plan = models.DateField(db_column='SIMPLE_DATE_PLAN')

    class Meta:
        managed = False
        db_table = 'VW_NURSE_WORK_LAB'


class NurseMedWork(models.Model):
    id = models.IntegerField(primary_key=True)
    num_history = models.CharField(max_length=25)
    doctor = models.CharField(max_length=255)
    patient = models.CharField(max_length=3064)
    medic_name = models.CharField(max_length=255)
    composite = models.CharField(max_length=512, db_column='DRUG_COMPOSIT')
    med_use = models.CharField(max_length=2200)
    datetime_plan = models.DateTimeField(db_column='DATE_PLAN')
    date_plan = models.DateField(db_column='SIMPLE_DATE_PLAN')
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')

    class Meta:
        managed = False
        db_table = 'VW_NURSE_WORK_MED'


class NurseExamWork(models.Model):
    id = models.IntegerField(primary_key=True)
    num_history = models.CharField(max_length=25)
    doctor = models.CharField(max_length=255)
    patient = models.CharField(max_length=255, db_column='LASTNAME')
    exam = models.CharField(max_length=255, db_column='GROUP_NAME')
    datetime_plan = models.DateTimeField(db_column='PLAN_DATETIME')
    date_plan = models.DateField(db_column='PLAN_DATE')
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')
    depart = models.CharField(max_length=255, db_column='DEPARTMENT')

    class Meta:
        managed = False
        db_table = 'VW_NURSE_WORK_EXAM'


class NurseProfViewWork(models.Model):
    id = models.IntegerField(primary_key=True)
    num_history = models.CharField(max_length=25)
    doctor = models.CharField(max_length=255)
    patient = models.CharField(max_length=255, db_column='LASTNAME')
    spec = models.CharField(max_length=255, db_column='SPECIALIZATION')
    datetime_plan = models.DateTimeField(db_column='PLAN_DATETIME')
    date_plan = models.DateField(db_column='PLAN_DATE')
    id_depart = models.IntegerField(db_column='ID_DEPARTMENT')
    depart = models.CharField(max_length=255, db_column='DEPARTNAME')

    class Meta:
        managed = False
        db_table = 'VW_NURSE_WORK_PROF'


class Hospitalization(models.Model):
    hosp_date = models.DateField(primary_key=True, db_column='OUT_DATE')
    cnt_extreme = models.IntegerField(db_column='OUT_CNT_EXTREME')
    cnt_plan = models.IntegerField(db_column='OUT_CNT_NORMAL')
    cnt_all = models.IntegerField(db_column='OUT_CNT_ALL')

    class Meta:
        managed = False
        db_table = 'GET_HOSPITALIZATION'


class WebUsersStat(models.Model):
    user_name = models.CharField(primary_key=True, max_length=80)
    cnt_system = models.IntegerField(db_column='CNT_SYSTEMUSER')
    cnt_web = models.IntegerField(db_column='CNT_CCONLINEUSER')

    class Meta:
        managed = False
        db_table = 'GET_CCONLINE_USER'


class ActiveMonitoringByHospital(models.Model):
    hospital = models.CharField(primary_key=True, max_length=255, db_column='GROUP_NAME')
    cnt_user = models.IntegerField(db_column='CNT_USER')

    class Meta:
        managed = False
        db_table = 'GET_ACTIVE_USER_BY_HOSPITAL'


class NurseAssign(models.Model):
    id = models.IntegerField(primary_key=True)
    type_app = models.IntegerField()  # TYPE_APP DMN_INTEGER,
    num_history = models.CharField(max_length=12) # NUM_HISTORY DMN_DOCUM,
    patient = models.CharField(max_length=2048) # PATIENT DMN_NAME,
    dt_appointment = models.DateTimeField() # DT_APPOINTMENT DMN_DATETIME_NULL,
    dt_nurse_exec = models.DateTimeField() # DT_NURSE_EXEC DMN_DATETIME_NULL,
    doctor = models.CharField(max_length=255) # DOCTOR DMN_NAME,
    nurse = models.CharField(max_length=255) # NURSE DMN_NAME,
    appointment = models.CharField(max_length=512) # APPOINTMENT DMN_TEXT512,
    appcomment = models.CharField(max_length=255) # APPCOMMENT DMN_NAME,
    department = models.CharField(max_length=255) # DEPARTMENT DMN_NAME,
    dt_cancel = models.DateTimeField() # DT_CANCEL DMN_DATETIME_NULL,
    out_code = models.CharField(max_length=255) # OUT_CODE DMN_NAME,
    is_cito = models.SmallIntegerField() # IS_CITO DMN_BOOLEAN

    class Meta:
        managed = False

def do_on_login(sender, user, request, **kwargs):
    """
    Обработка сигнала авторизации пользователя
    :param sender:
    :param user:
    :param request:
    :param kwargs:
    :return:
    """
    remote_address = request.META['REMOTE_ADDR']
    sql = "INSERT INTO USER_LOGINS (USR, DATE_LOGIN, MACHINEIP, OPER) VALUES('%s', 'now', '%s', 3)" \
          % (user, remote_address)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


# подписка на сигнал
user_logged_in.connect(do_on_login)
