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
