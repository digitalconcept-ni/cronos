from django.db import models
from django.forms import model_to_dict

from core.user.models import User


# Create your models here.

class Departament(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Nombre del Departamento')

    class Meta:
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def toLIST(self):
        item = [
            self.id, self.name
        ]
        return item


class Career(models.Model):
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, verbose_name='Nombre', null=True)
    code = models.CharField(max_length=7, unique=True, verbose_name='Codigo', null=True)

    class Meta:
        verbose_name = 'carrera'
        verbose_name_plural = 'carreras'
        ordering = ['-id']

    def __str__(self):
        return f'{self.departament.name} - {self.name} - {self.code}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def toLIST(self):
        item = [
            self.id, self.departament.name, self.name, self.code, self.id
        ]
        return item


class Pensum(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, verbose_name='Nombre', null=True)

    class Meta:
        verbose_name = 'pensum'
        verbose_name_plural = 'pensums'
        ordering = ['-id']

    def __str__(self):
        return f'{self.career} - {self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def toLIST(self):
        item = [
            self.id, self.career.__str__(), self.name
        ]
        return item


"""
Clase para crear la table de asignatura
"""


class Subject(models.Model):
    pensum = models.ForeignKey(Pensum, on_delete=models.CASCADE, verbose_name='Pensum', null=True)
    code = models.CharField(max_length=5, unique=True, verbose_name='Numero de carnet', null=True)
    name = models.CharField(max_length=50, verbose_name='Nombre asignatura', null=True)
    description = models.CharField(max_length=100, verbose_name='Descripcion', null=True)

    class Meta:
        verbose_name = 'asignatura'
        verbose_name_plural = 'asignaturas'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} - {self.code}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def toLIST(self):
        item = [
            self.id, self.pensum.__str__(), self.code, self.name, self.description
        ]
        return item


"""
Tabla auxiliar que nos permite relacionar que usuario en este caso el profesor
puede dar 1 o mas clases
"""


class UserSubject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario', null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Asignatura', null=True)

    class Meta:
        verbose_name = 'usuario_asignatura'
        verbose_name_plural = 'usuarios_asignaturas'
        ordering = ['subject']


class Classroom(models.Model):
    CLASSROOM_CHOICE = [
        ('LAB', 'Laboratorio'),
        ('PAR', 'Particular'),
        ('AUD', 'Auditorio'),
    ]
    name = models.CharField(max_length=50, verbose_name='Nombre', null=True)
    type = models.CharField(max_length=3, choices=CLASSROOM_CHOICE, verbose_name='Tipo', null=True)
    building = models.CharField(max_length=50, verbose_name='Edificio', null=True)
    status = models.BooleanField(default=True, verbose_name='Estado', null=True)

    class Meta:
        verbose_name = 'aula'
        verbose_name_plural = 'aulas'
        ordering = ['status']

    def __str__(self):
        return f'{self.name} {self.get_type_display()}'

    def toLIST(self):
        item = [
            self.id, self.name, self.get_type_display(), self.building, self.status,
        ]
        return item

    def toJSON(self):
        item = model_to_dict(self)
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
    career = models.ForeignKey(Career, on_delete=models.CASCADE, verbose_name='Carrera', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario', null=True)
    turn = models.CharField(max_length=3, choices=TURN_CHOICE, verbose_name='Turno', null=True)
    mode = models.CharField(max_length=3, choices=MODE_CHOICE, verbose_name='Modalidad', null=True)

    class Meta:
        verbose_name = 'inscripcion'
        verbose_name_plural = 'inscripciones'
        ordering = ['career']


class Grupos(models.Model):
    code = models.CharField(max_length=7, null=True, verbose_name="Codigo")
    name = models.CharField(max_length=50, verbose_name='Nombre', null=True)

    class Meta:
        verbose_name = 'grupo'
        verbose_name_plural = 'grupos'
        ordering = ['code']

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def toLIST(self):
        item = [
            self.id, self.code, self.name, self.id
        ]
        return item


class InscriptionSubject(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, verbose_name='Inscripcion', null=True)
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, verbose_name='Grupo', null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='Aula', null=True)
    user_subject = models.ForeignKey(UserSubject, on_delete=models.CASCADE, verbose_name='Asignatura',
                                     null=True)  # Relacion con
    date_start = models.DateField(verbose_name='Fecha inicio', null=True)
    date_end = models.DateField(verbose_name='Fecha fin', null=True)
    time_start = models.TimeField(verbose_name='Hora inicio', null=True)
    time_end = models.TimeField(verbose_name='Hora fin', null=True)

    class Meta:
        verbose_name = 'inscriptionsubect'
        verbose_name_plural = 'inscriptionssubects'
        ordering = ['-date_start']


class attendanceSubject(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, verbose_name='Inscripcion', null=True)
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE, verbose_name='Grupo', null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='Aula', null=True)
    user_subject = models.ForeignKey(UserSubject, on_delete=models.CASCADE, verbose_name='Asignatura',
                                     null=True)  # Relacion con
    date_start = models.DateField(verbose_name='Fecha inicio', null=True)
    date_end = models.DateField(verbose_name='Fecha fin', null=True)
    time_start = models.TimeField(verbose_name='Hora inicio', null=True)
    time_end = models.TimeField(verbose_name='Hora fin', null=True)

    class Meta:
        verbose_name = 'inscriptionsubect'
        verbose_name_plural = 'inscriptionssubects'
        ordering = ['-date_start']


