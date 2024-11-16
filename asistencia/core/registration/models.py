from django.db import models
from django.forms import model_to_dict

from core.user.models import User


# Create your models here.

class Departament(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'

class Career(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    code = models.CharField(max_length=7, unique=True, verbose_name='Codigo')

    class Meta:
        verbose_name = 'carrera'
        verbose_name_plural = 'carreras'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} - {self.code}'


class Pensum(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        verbose_name = 'pensum'
        verbose_name_plural = 'pensums'
        ordering = ['-id']

    def __str__(self):
        return f'{self.career} - {self.name}'


"""
Clase para crear la table de asignatura
"""


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    pensum = models.ForeignKey(Pensum, on_delete=models.CASCADE, verbose_name='Pensum')
    code = models.CharField(max_length=5, unique=True, verbose_name='Numero de carnet')
    name = models.CharField(max_length=50, verbose_name='Nombre asignatura')
    description = models.CharField(max_length=100, verbose_name='Descripcion')

    class Meta:
        verbose_name = 'asignatura'
        verbose_name_plural = 'asignaturas'
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} - {self.code}'

class Classroom(models.Model):
    CLASSROOM_CHOICE = [
        ('LAB', 'Laboratorio'),
        ('PAR', 'Particular'),
        ('AUD', 'Auditorio'),
    ]
    name = models.CharField(max_length=50, verbose_name='Nombre')
    type = models.CharField(max_length=3, choices=CLASSROOM_CHOICE, verbose_name='Tipo')
    building = models.CharField(max_length=50, verbose_name='Edificio')
    status = models.BooleanField(default=True, verbose_name='Estado')

    class Meta:
        verbose_name = 'aula'
        verbose_name_plural = 'aulas'
        ordering = ['status']

    def __str__(self):
        return f'{self.name} {self.get_type_display()}'


    def toJSON(self):
        item  = model_to_dict(self)
        item['type'] = self.get_type_display()
        return item

class Inscription(models.Model):
    TURN_CHOICE = [
        ('DOM', 'Dominical'),
        ('SAB', 'Sabatino'),
        ('DIU', 'Diurno'),
        ('VES', 'Vespertino'),
        ('NOC', 'Nocturno'),
    ]
    MODE_CHOICE = [
        ('REG', 'Regular'),
        ('ENC', 'Encuentro'),
    ]
    career = models.ForeignKey(Career, on_delete=models.CASCADE, verbose_name='Carrera')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Asignatura')
    aula = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='Asignatura')
    date_start = models.DateField(verbose_name='Fecha inicio')
    date_end = models.DateField(verbose_name='Fecha fin')
    time_start = models.TimeField(verbose_name='Hora inicio')
    time_end = models.TimeField(verbose_name='Hora fin')
    turn = models.CharField(max_length=3, choices=TURN_CHOICE, verbose_name='Turno')
    mode = models.CharField(max_length=3, choices=MODE_CHOICE, verbose_name='Modalidad')

    class Meta:
        verbose_name = 'inscripcion'
        verbose_name_plural = 'inscripciones'
        ordering = ['-date_start']