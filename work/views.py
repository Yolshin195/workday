from datetime import datetime, UTC

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from .models import Workday
from .models import Task
from .forms import TaskForm


def list_work_day(request):
    current_month = datetime.now(UTC).month
    current_year = datetime.now(UTC).year

    # Получение всех рабочих дней за текущий месяц
    workdays_in_current_month = Workday.objects.filter(
        Q(day__month=current_month, day__year=current_year)
    )

    context = {"workdays_in_current_month": workdays_in_current_month}
    return render(request, "work/list_work_day.html", context)


class CurrentWorkDayView(View):
    template_name = 'work/current_workday.html'

    def get(self, request, year=None, month=None, day=None):
        # Получаем текущий день
        today = datetime(year, month, day, tzinfo=UTC) if year and month and day else datetime.now(UTC)

        # Пытаемся найти сущность текущего рабочего дня
        workday, created = Workday.objects.get_or_create(day=today)
        tasks = workday.task_set.all()

        progress = 12.5 * workday.total_worked_hours

        # Передаем сущность в шаблон
        context = {'workday': workday, 'tasks': tasks, 'progress': progress}
        return render(request, self.template_name, context)


def begin_workday(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            workday = Workday.objects.get(id=pk)
            if workday:
                workday.begin = datetime.now(UTC)
                workday.save()

    return redirect('current_workday')


def end_workday(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            workday = Workday.objects.get(id=pk)
            if workday:
                workday.end = datetime.now(UTC)
                workday.save()

    return redirect('current_workday')


def create_task(request):
    TaskForm(request)
    return redirect('current_workday')


def begin_task(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            task = Task.objects.get(id=pk)
            if task:
                task.begin = datetime.now(UTC)
                task.save()

    return redirect('current_workday')


def end_task(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            task = Task.objects.get(id=pk)
            if task:
                task.end = datetime.now(UTC)
                task.save()

    return redirect('current_workday')


def delete_task(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            task = Task.objects.get(id=pk)
            if task:
                task.delete()

    return redirect('current_workday')
