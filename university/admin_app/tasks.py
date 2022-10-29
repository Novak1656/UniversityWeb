import io
import xlsxwriter
from celery import shared_task
from django.http import HttpResponse
from rest_framework.response import Response

from .models import StudyDirection
from curator_app.models import StudyGroup
from django.db.models import When, Count, IntegerField, Case, Sum


@shared_task
def generate_report():
    def translate_sex(sex_value):
        sex_dict = {'Man': 'Мужчина', 'Woman': 'Женщина'}
        return sex_dict.get(sex_value)

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, options={'in_memory': True})

    # Columns formats
    merge_format = workbook.add_format({'align': 'center'})
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')

    # Create directions report list
    directions_data = StudyDirection.objects.select_related('curator').prefetch_related('disciplines').all()
    directions_sheet_labels = [
        ('A1:A2', 'Направление'),
        ('B1:B2', 'Дисциплины'),
        ('C1:E1', 'Куратор'),
        ('C2', 'ФИО'),
        ('D2', 'Пол'),
        ('E2', 'Возраст')
    ]
    directions_sheet = workbook.add_worksheet(name='Directions')

    for col_param, label in directions_sheet_labels:
        if ':' in col_param:
            directions_sheet.merge_range(col_param, label, merge_format)
            directions_sheet.set_column(col_param, 30)
            continue
        directions_sheet.write(col_param, label, merge_format)

    for i, direction in enumerate(directions_data, start=2):
        disciplines = '\n'.join(f'{num}. {obj.title}' for num, obj in enumerate(direction.disciplines.all(), start=1))
        curator = direction.curator
        row_data = [direction.title, disciplines, curator.get_full_name(), translate_sex(curator.sex), curator.old]
        for col, value in enumerate(row_data):
            directions_sheet.write(i, col, value, cell_format)

    # Create groups report list
    groups_data = StudyGroup.objects.prefetch_related('students').all()
    groups_sheet_labels = [
        ('A1', 'Группа'),
        ('B1', 'Студенты'),
        ('C1', 'Мужчин'),
        ('D1', 'Женщин'),
        ('E1', 'Свободных мест')
    ]
    groups_sheet = workbook.add_worksheet(name='Groups')
    groups_sheet.set_column('A1:E2', 30)

    for col_param, label in groups_sheet_labels:
        groups_sheet.write(col_param, label, merge_format)

    for i, group in enumerate(groups_data, start=1):
        students = group.students.all()
        if students.exists():
            students_list = '\n'.join(f'{num}. {obj.get_full_name()}' for num, obj in enumerate(students, start=1))
            mw_count_data = students.annotate(
                is_man=Count(Case(When(sex='Man', then=1), output_field=IntegerField())),
                is_woman=Count(Case(When(sex='Woman', then=1), output_field=IntegerField()))
            ).aggregate(
                mans=Sum('is_man'),
                womans=Sum('is_woman')
            )
            free_places = 20 - group.students_count
            row_data = [group.title, students_list, mw_count_data.get('mans'), mw_count_data.get('womans'), free_places]
            for col, value in enumerate(row_data):
                groups_sheet.write(i, col, value, cell_format)
            continue
        row_data = [group.title, 'Студентов нет', 0, 0, 20]
        for col, value in enumerate(row_data):
            groups_sheet.write(i, col, value, cell_format)

    workbook.close()

    output.seek(0)
    response = Response(HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ))
    print(response)
    response['Content-Disposition'] = "attachment; filename=UniversityReport.xlsx"
    return response
