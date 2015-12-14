# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, Textarea, TextInput, DateTimeInput, HiddenInput
from models import Diary


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('diary_name', 'diary_date', 'diary_text', 'id_history', 'id_depart', 'id_doctor')
        labels = {
            'diary_name': u'Совместный осмотр',
            'diary_date': u'Дата осмотра',
            'diary_text': u'Запись осмотра',
        }
        widgets = {
            'diary_name': TextInput(attrs={'class': 'form-control'}),
            'diary_date': DateTimeInput(attrs={'class': 'form-control', 'input_formats': '%Y-%m-%d %H:%M:%S'}),
            'diary_text': Textarea(attrs={'cols': 80, 'rows': 10, 'class': 'form-control'}),
            'id_history': HiddenInput(),
            'id_depart': HiddenInput(),
            'id_doctor': HiddenInput(),
        }
