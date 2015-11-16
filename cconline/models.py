from django.db import models

# Create your models here.


class Departments(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'departments'


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
