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
