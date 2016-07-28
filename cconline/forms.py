# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, Textarea, TextInput, DateTimeInput, HiddenInput
from models import Diary
from django.db import models


class DiaryForm(forms.ModelForm):
    # patient = forms.CharField(max_length=255, label='Пациент', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
    depart = forms.CharField(max_length=255, label='Отделение', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))

    class Meta:
        model = Diary
        fields = ['id','diary_name', 'diary_date', 'diary_text', 'id_history', 'id_depart', 'id_doctor', 'depart']
        labels = {
            'diary_name': u'Совместный осмотр',
            'diary_date': u'Дата осмотра',
            'diary_text': u'Запись осмотра',
            'depart': u'Отделение'
        }
        widgets = {
            'diary_name': TextInput(attrs={'class': 'form-control'}),
            'diary_date': DateTimeInput(attrs={'class': 'form-control', 'input_formats': '%Y-%m-%d %H:%M:%S'}),
            'diary_text': Textarea(attrs={'cols': 80, 'rows': 10, 'class': 'form-control', 'required': 'required'}),
            'id_history': HiddenInput(),
            'id_depart': HiddenInput(),
            'id_doctor': HiddenInput(),
            'id': HiddenInput(),
            'depart': TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'depart',
            'diary_name',
            'diary_date',
            'diary_text',
            'id_history',
            'id_depart',
            'id_doctor',
            'id_history',
        ]