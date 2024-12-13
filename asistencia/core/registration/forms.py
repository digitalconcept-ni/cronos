from django import forms
from django.forms import ModelForm

from core.registration.models import *


class DepartamentForm(ModelForm):
    class Meta:
        model = Departament
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CareerForm(ModelForm):
    class Meta:
        model = Career
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PensumForm(ModelForm):
    class Meta:
        model = Pensum
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserSubjectForm(ModelForm):
    class Meta:
        model = UserSubject
        fields = '__all__'
        widgets = {
            # 'user': forms.Select(attrs={
            #     'class': 'custom-select select2',
            #     # 'style': 'width: 100%'
            # }),
            'user': forms.Select(attrs={'class': 'form-control select2'}),
        }


    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class InscriptionForm(ModelForm):

    class Meta:
        model = Inscription
        fields = '__all__'

class InscriptionSubjectForm(ModelForm):

    class Meta:
        model = InscriptionSubject
        fields = '__all__'
