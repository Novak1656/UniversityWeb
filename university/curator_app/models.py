from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Curator(models.Model):
    SEX_LIST = [('Man', 'Мужчина'), ('Woman', 'Женщина')]

    first_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255
    )
    second_name = models.CharField(
        verbose_name='Имя',
        max_length=255
    )
    last_name = models.CharField(
        verbose_name='Отчество',
        max_length=255,
        blank=True
    )
    sex = models.CharField(
        verbose_name='Пол',
        choices=SEX_LIST,
        max_length=10
    )
    old = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        blank=True,
    )

    class Meta:
        verbose_name = 'Куратор'
        verbose_name_plural = 'Кураторы'

    def get_full_name(self):
        return f'{self.first_name} {self.second_name} {self.last_name}'

    def __str__(self):
        return f'{self.get_full_name()}'


class StudyGroup(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    direction = models.ForeignKey(
        verbose_name='Направление',
        to='admin_app.StudyDirection',
        on_delete=models.PROTECT,
        related_name='groups'
    )
    students_count = models.IntegerField(
        verbose_name='Кол-во студентов',
        default=0,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(0)
        ]
    )

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'
        ordering = ['-title']

    def __str__(self):
        return f'{self.title}'


class Student(models.Model):
    SEX_LIST = [('Man', 'Мужчина'), ('Woman', 'Женщина')]

    first_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255
    )
    second_name = models.CharField(
        verbose_name='Имя',
        max_length=255
    )
    last_name = models.CharField(
        verbose_name='Отчество',
        max_length=255,
        blank=True
    )
    sex = models.CharField(
        verbose_name='Пол',
        choices=SEX_LIST,
        max_length=10
    )
    group = models.ForeignKey(
        verbose_name='Группа',
        to=StudyGroup,
        on_delete=models.PROTECT,
        related_name='students'
    )
    year_of_admission = models.DateField(
        verbose_name='Дата поступления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['-group']

    def get_full_name(self):
        return f'{self.first_name} {self.second_name} {self.last_name}'

    def __str__(self):
        return f'{self.get_full_name}: {self.group}'
