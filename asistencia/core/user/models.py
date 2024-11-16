from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
# from crum import get_current_request
from config import settings


class User(AbstractUser):
    ROll_CHOICES = (
        ('student', 'Estudiante'),
        ('teacher', 'Profesor'),
    )
    GENDER_CHOICES = (
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO'),
    )
    roll = models.CharField(max_length=10, default='student', choices=ROll_CHOICES, verbose_name="Roll")
    phone_number = models.CharField(max_length=8, null=True, verbose_name='Numero de telefono')
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES, verbose_name='Genero')
    code = models.CharField(max_length=7, null=True, verbose_name="Codigo")
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def __str__(self):
        return f'{self.username}'

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/empty.png'

    def toLIST(self):
        last_login = ' ' if self.last_login is None else self.last_login.strftime('%Y-%m-%d')
        groups = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        data = [
            self.id, self.get_full_name(), self.username, self.phone_number, self.date_joined.strftime('%Y-%m-%d'),
            self.get_image(), self.is_superuser, last_login, self.is_active,
            groups, self.presale
        ]
        return data

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        item['last_login'] = '' if self.last_login is None else self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    # def get_group_session(self):
    #     try:
    #         request = get_current_request()
    #         groups = self.groups.all()
    #         if groups.exists():
    #             if 'group' not in request.session:
    #                 request.session['group'] = groups[0]
    #     except:
    #         pass
