import random

from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
    Subject,
)


def find_schoolkid(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f'Ученик с именем {schoolkid_name} не найден, уточните имя.')
    except Schoolkid.MultipleObjectsReturned:
        print(f'Найдено несколько учеников с именем {schoolkid_name}, уточните имя.')


def find_subject(subject_title, schoolkid):
    try:
        return Subject.objects.get(
            title=subject_title,
            year_of_study=schoolkid.year_of_study
        )
    except Subject.DoesNotExist:
        print(f'Предмет под названием {subject_title} не найден, уточните название предмета.')


def fix_marks(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    schoolkid_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in schoolkid_marks:
        mark.points = 5
        mark.save()
    print('Оценки исправлены!')


def remove_chastisements(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    schoolkid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    schoolkid_chastisements.delete()
    print('Замечания удалены!')


def create_commendation(schoolkid_name, subject_title):
    schoolkid = find_schoolkid(schoolkid_name)
    subject = find_subject(subject_title, schoolkid)
    commendation_phrases = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Так держать!',
        'Ты на верном пути!',
        'Великолепно',
    ]
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subject
    )
    schoolkid_commendations = Commendation.objects.filter(
        schoolkid=schoolkid,
        subject=subject
    )
    commendation_dates = [i.created for i in schoolkid_commendations]
    lessons_without_commendation = lessons.exclude(date__in=commendation_dates)
    lesson_to_commend = lessons_without_commendation.order_by('-date').first()
    Commendation.objects.create(
        schoolkid=schoolkid,
        teacher=lesson_to_commend.teacher,
        subject=lesson_to_commend.subject,
        created=lesson_to_commend.date,
        text=random.choice(commendation_phrases)
    )
    print('Похвала добавлена!')
