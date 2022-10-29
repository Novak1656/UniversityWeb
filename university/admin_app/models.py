from django.db import models
from django.utils.timezone import now


class StudyDirection(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    curator = models.OneToOneField(
        verbose_name='Куратор',
        to='curator_app.Curator',
        on_delete=models.PROTECT,
        related_name='direction'
    )
    disciplines = models.ManyToManyField(
        verbose_name='Дисциплины',
        to='StudyDiscipline',
        related_name='directions'
    )

    class Meta:
        verbose_name = 'Направление подготовки'
        verbose_name_plural = 'Направления подготовки'
        ordering = ['-title']

    def __str__(self):
        return f'{self.title}'


class StudyDiscipline(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    class Meta:
        verbose_name = 'Учебная дисциплина'
        verbose_name_plural = 'Учебные дисциплины'
        ordering = ['-title']

    def __str__(self):
        return f'{self.title}'
