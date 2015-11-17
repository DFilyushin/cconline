from django.db import models

# Create your models here.


class Departments(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'departments'

class ClassMkb(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    parent_id = models.IntegerField(db_column='PARENT_ID', blank=True, null=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=1020, blank=True) # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=200, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'class_mkb'


class RefSocial(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True) # Field name made lowercase.
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True) # Field name made lowercase.
    last_user = models.CharField(db_column='LAST_USER', max_length=320, blank=True) # Field name made lowercase.
    last_date = models.DateTimeField(db_column='LAST_DATE', blank=True, null=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', unique=True, max_length=1020) # Field name made lowercase.
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'ref_social'


class RefNationality(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    name_rus = models.CharField(db_column='NAME_RUS', unique=True, max_length=1020) # Field name made lowercase.
    name_kaz = models.CharField(db_column='NAME_KAZ', max_length=1020) # Field name made lowercase.
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True) # Field name made lowercase.
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True) # Field name made lowercase.
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'ref_nationality'


class RefBenefit(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True) # Field name made lowercase.
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', unique=True, max_length=1020) # Field name made lowercase.
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'ref_benefit'


class RefCity(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    id_parent = models.IntegerField(db_column='ID_PARENT', blank=True, null=True) # Field name made lowercase.
    k = models.IntegerField(db_column='K', blank=True, null=True) # Field name made lowercase.
    name_rus = models.CharField(db_column='NAME_RUS', max_length=1020, blank=True) # Field name made lowercase.
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True) # Field name made lowercase.
    is_city = models.SmallIntegerField(db_column='IS_CITY', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'ref_city'


class History(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    rdt_create = models.DateTimeField(db_column='RDT_CREATE', blank=True, null=True) # Field name made lowercase.
    ru_create = models.CharField(db_column='RU_CREATE', max_length=320, blank=True) # Field name made lowercase.
    last_date = models.DateTimeField(db_column='LAST_DATE', blank=True, null=True) # Field name made lowercase.
    last_user = models.CharField(db_column='LAST_USER', max_length=320, blank=True) # Field name made lowercase.
    lastname = models.CharField(db_column='LASTNAME', max_length=1020, blank=True) # Field name made lowercase.
    firstname = models.CharField(db_column='FIRSTNAME', max_length=1020, blank=True) # Field name made lowercase.
    middlename = models.CharField(db_column='MIDDLENAME', max_length=1020, blank=True) # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True) # Field name made lowercase.
    gender = models.SmallIntegerField(db_column='GENDER', blank=True, null=True) # Field name made lowercase.
    iin = models.CharField(db_column='IIN', max_length=48, blank=True) # Field name made lowercase.
    bar_code = models.CharField(db_column='BAR_CODE', max_length=48, blank=True) # Field name made lowercase.
    live_address = models.CharField(db_column='LIVE_ADDRESS', max_length=1020, blank=True) # Field name made lowercase.
    insurence_company = models.CharField(db_column='INSURENCE_COMPANY', max_length=1020, blank=True) # Field name made lowercase.
    insurence_number = models.CharField(db_column='INSURENCE_NUMBER', max_length=100, blank=True) # Field name made lowercase.
    med_reg_number = models.CharField(db_column='MED_REG_NUMBER', max_length=100, blank=True) # Field name made lowercase.
    id_social = models.ForeignKey('RefSocial', db_column='ID_SOCIAL', blank=True, null=True) # Field name made lowercase.
    id_nationality = models.ForeignKey('RefNationality', db_column='ID_NATIONALITY', blank=True, null=True) # Field name made lowercase.
    id_benefit = models.ForeignKey('RefBenefit', db_column='ID_BENEFIT', blank=True, null=True) # Field name made lowercase.
    id_city = models.ForeignKey('RefCity', db_column='ID_CITY', blank=True, null=True) # Field name made lowercase.
    workplace = models.CharField(db_column='WORKPLACE', max_length=2048, blank=True) # Field name made lowercase.
    study = models.CharField(db_column='STUDY', max_length=2048, blank=True) # Field name made lowercase.
    num_history = models.CharField(db_column='NUM_HISTORY', max_length=100, blank=True) # Field name made lowercase.
    receipt = models.DateTimeField(db_column='RECEIPT', blank=True, null=True) # Field name made lowercase.
    extreme_type = models.SmallIntegerField(db_column='EXTREME_TYPE', blank=True, null=True) # Field name made lowercase.
    id_type_hospitalize = models.IntegerField(db_column='ID_TYPE_HOSPITALIZE', blank=True, null=True) # Field name made lowercase.
    id_depart = models.ForeignKey(Departments, db_column='ID_DEPART', blank=True, null=True) # Field name made lowercase.
    id_doctor = models.IntegerField() # Field name made lowercase.
    chamber = models.CharField(db_column='CHAMBER', max_length=1020, blank=True) # Field name made lowercase.
    id_incoming_diag = models.ForeignKey(ClassMkb, db_column='ID_INCOMING_DIAG', blank=True, null=True, related_name='+') # Field name made lowercase.
    incoming_diag = models.CharField(db_column='INCOMING_DIAG', max_length=4096, blank=True) # Field name made lowercase.
    id_clinic_diag = models.ForeignKey(ClassMkb, db_column='ID_CLINIC_DIAG', blank=True, null=True, related_name='+') # Field name made lowercase.
    id_lpu_diag = models.ForeignKey(ClassMkb, db_column='ID_LPU_DIAG', blank=True, null=True) # Field name made lowercase.
    diag_lpu = models.CharField(db_column='DIAG_LPU', max_length=4096, blank=True) # Field name made lowercase.
    id_related_diag = models.ForeignKey(ClassMkb, db_column='ID_RELATED_DIAG', blank=True, null=True, related_name='+') # Field name made lowercase.
    related_diagnosis = models.CharField(db_column='RELATED_DIAGNOSIS', max_length=4096, blank=True) # Field name made lowercase.
    id_main_diag = models.IntegerField(db_column='ID_MAIN_DIAG', blank=True, null=True) # Field name made lowercase.
    id_compl_diag = models.IntegerField(db_column='ID_COMPL_DIAG', blank=True, null=True) # Field name made lowercase.
    id_end_diag = models.IntegerField(db_column='ID_END_DIAG', blank=True, null=True) # Field name made lowercase.
    id_from = models.IntegerField() # Field name made lowercase.
    type_warior = models.IntegerField(db_column='TYPE_WARIOR', blank=True, null=True) # Field name made lowercase.
    discharge = models.DateTimeField(db_column='DISCHARGE', blank=True, null=True) # Field name made lowercase.
    id_cancer_treatment = models.IntegerField() # Field name made lowercase.
    baby_massa = models.DecimalField(db_column='BABY_MASSA', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    baby_length = models.DecimalField(db_column='BABY_LENGTH', max_digits=15, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    hosp_with_mother = models.SmallIntegerField(db_column='HOSP_WITH_MOTHER', blank=True, null=True) # Field name made lowercase.
    hosp_hour_after_disease = models.IntegerField(db_column='HOSP_HOUR_AFTER_DISEASE', blank=True, null=True) # Field name made lowercase.
    id_result = models.IntegerField() # Field name made lowercase.
    id_treatment_effect = models.IntegerField(db_column='ID_TREATMENT_EFFECT', blank=True, null=True) # Field name made lowercase.
    main_diag = models.CharField(db_column='MAIN_DIAG', max_length=4096, blank=True) # Field name made lowercase.
    main_complication = models.CharField(db_column='MAIN_COMPLICATION', max_length=4096, blank=True) # Field name made lowercase.
    send_to = models.CharField(db_column='SEND_TO', max_length=1020, blank=True) # Field name made lowercase.
    date_set_diag = models.DateTimeField(db_column='DATE_SET_DIAG', blank=True, null=True) # Field name made lowercase.
    is_delete = models.SmallIntegerField(db_column='IS_DELETE', blank=True, null=True) # Field name made lowercase.
    id_lpu = models.IntegerField() # Field name made lowercase.
    archive_send = models.DateField(db_column='ARCHIVE_SEND', blank=True, null=True) # Field name made lowercase.
    is_signed = models.SmallIntegerField(db_column='IS_SIGNED', blank=True, null=True) # Field name made lowercase.
    who_signed = models.CharField(db_column='WHO_SIGNED', max_length=320, blank=True) # Field name made lowercase.
    id_bedregime = models.IntegerField() # Field name made lowercase.
    clinic_diag = models.CharField(db_column='CLINIC_DIAG', max_length=4096, blank=True) # Field name made lowercase.
    type_card = models.IntegerField(db_column='TYPE_CARD', blank=True, null=True) # Field name made lowercase.
    viral_diseases = models.CharField(db_column='VIRAL_DISEASES', max_length=2048, blank=True) # Field name made lowercase.
    chronic_diseases = models.CharField(db_column='CHRONIC_DISEASES', max_length=2048, blank=True) # Field name made lowercase.
    preliminary_diag = models.CharField(db_column='PRELIMINARY_DIAG', max_length=4096, blank=True) # Field name made lowercase.
    drug_intolerance = models.CharField(db_column='DRUG_INTOLERANCE', max_length=2048, blank=True) # Field name made lowercase.
    id_typepay = models.IntegerField() # Field name made lowercase.
    date_first_view = models.DateTimeField(db_column='DATE_FIRST_VIEW', blank=True, null=True) # Field name made lowercase.
    id_finance = models.IntegerField() # Field name made lowercase.
    id_ext_doctor_view = models.IntegerField(db_column='ID_EXT_DOCTOR_VIEW', blank=True, null=True) # Field name made lowercase.
    date_first_view_ext = models.DateTimeField(db_column='DATE_FIRST_VIEW_EXT', blank=True, null=True) # Field name made lowercase.
    id_initnurse = models.IntegerField(db_column='ID_INITNURSE', blank=True, null=True) # Field name made lowercase.
    is_view = models.SmallIntegerField(db_column='IS_VIEW', blank=True, null=True) # Field name made lowercase.
    go_cardiosurgery = models.DateTimeField(db_column='GO_CARDIOSURGERY', blank=True, null=True) # Field name made lowercase.
    go_reahab = models.DateTimeField(db_column='GO_REAHAB', blank=True, null=True) # Field name made lowercase.
    id_bedtype = models.IntegerField(db_column='ID_BEDTYPE', blank=True, null=True) # Field name made lowercase.
    type_trauma = models.SmallIntegerField(db_column='TYPE_TRAUMA', blank=True, null=True) # Field name made lowercase.
    id_patient_sender = models.IntegerField(db_column='ID_PATIENT_SENDER', blank=True, null=True) # Field name made lowercase.
    type_hospit = models.SmallIntegerField(db_column='TYPE_HOSPIT', blank=True, null=True) # Field name made lowercase.
    count_hospit_inyear = models.SmallIntegerField(db_column='COUNT_HOSPIT_INYEAR', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'history'


class ListHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    num_history = models.CharField(max_length=25)
    lastname = models.CharField(max_length=255)
    depart_name = models.CharField(max_length=255)
    dob = models.DateField()
    yearof = models.IntegerField()
    receipt = models.DateTimeField()
    discharge = models.DateTimeField()
    id_doctor = models.IntegerField()
    id_depart = models.IntegerField()

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
    blob_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'VW_DIARY'


class ListAnalysis(models.Model):
    id = models.IntegerField(primary_key=True) # Field name made lowercase.
    id_history = models.IntegerField()
    id_doctor = models.IntegerField()
    id_labanalysis = models.CharField(max_length=10)
    date_assign = models.DateTimeField(db_column='DATE_ASSIGN', blank=True, null=True) # Field name made lowercase.
    date_plan = models.DateTimeField(db_column='DATE_PLAN', blank=True, null=True) # Field name made lowercase.
    id_executer = models.IntegerField(db_column='ID_EXECUTER', blank=True, null=True) # Field name made lowercase.
    date_execute = models.DateTimeField(db_column='DATE_EXECUTE', blank=True, null=True) # Field name made lowercase.
    id_nurse_execute = models.IntegerField(db_column='ID_NURSE_EXECUTE', blank=True, null=True) # Field name made lowercase.
    nurse_date_execute = models.DateTimeField(db_column='NURSE_DATE_EXECUTE', blank=True, null=True) # Field name made lowercase.
    id_med_cancel = models.IntegerField(db_column='ID_MED_CANCEL', blank=True, null=True) # Field name made lowercase.
    cancel_cause = models.CharField(db_column='CANCEL_CAUSE', max_length=1020, blank=True) # Field name made lowercase.
    is_cito = models.SmallIntegerField(db_column='IS_CITO', blank=True, null=True) # Field name made lowercase.
    lab_comment = models.CharField(db_column='LAB_COMMENT', max_length=4096, blank=True) # Field name made lowercase.
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
        managed=False
        db_table = 'VW_PAIN_STATUS'

