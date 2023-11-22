from collections import namedtuple
from datetime import datetime, UTC

from django.db.models import Q, Func, F
from django.shortcuts import render, redirect
from django.views import View

from .models import Workday
from .models import Task
from .forms import TaskForm
import calendar

Day = namedtuple('Day', ['day', 'today', 'selected', 'tasks_exist'])


class MonthFilter:
    def __init__(self, year=None, month=None, day=None):
        self.today = datetime.now(UTC)
        self.selected_date = datetime(year, month, day, tzinfo=UTC) if year and month and day else None
        self.month_name = self.today.strftime("%B")
        self.monthcalendar = calendar.monthcalendar(self.today.year, self.today.month)
        self.workdays = self.workdays_in_select_month(self.today if self.selected_date is None else self.selected_date)

    @staticmethod
    def workdays_in_select_month(date: datetime) -> list[int]:
        workdays_in_current_month = Workday.objects.filter(
            Q(day__month=date.month, day__year=date.year)
        )
        return [workday.day.day for workday in workdays_in_current_month]


class ListWorkdayView(View):
    template_name = 'work/list_workday.html'

    def get(self, request, year=None, month=None, day=None):
        month_filter = MonthFilter(year, month, day)

        context = {
            "month_filter": month_filter
        }
        return render(request, self.template_name, context)


class CurrentWorkDayView(View):
    template_name = 'work/current_workday.html'

    def get(self, request, year=None, month=None, day=None):
        # Получаем текущий день
        today = datetime(year, month, day, tzinfo=UTC) if year and month and day else datetime.now(UTC)

        # Пытаемся найти сущность текущего рабочего дня
        workday, created = Workday.objects.get_or_create(day=today)
        tasks = workday.task_set.all()

        progress = 12.5 * workday.total_worked_hours

        month_filter = MonthFilter(year, month, day)

        # Передаем сущность в шаблон
        context = {
            'workday': workday,
            'tasks': tasks,
            'progress': progress,
            'month_filter': month_filter
        }
        return render(request, self.template_name, context)


def begin_workday(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            workday = Workday.objects.get(id=pk)
            if workday:
                workday.begin = datetime.now(UTC)
                workday.save()

    return redirect(request.META.get('HTTP_REFERER'))


def end_workday(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            workday = Workday.objects.get(id=pk)
            if workday:
                workday.end = datetime.now(UTC)
                workday.save()

    return redirect(request.META.get('HTTP_REFERER'))


def create_task(request):
    TaskForm(request)
    return redirect(request.META.get('HTTP_REFERER'))


def begin_task(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            task = Task.objects.get(id=pk)
            if task:
                task.begin = datetime.now(UTC)
                task.save()

    return redirect(request.META.get('HTTP_REFERER'))


def end_task(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            task = Task.objects.get(id=pk)
            if task:
                task.end = datetime.now(UTC)
                task.save()

    return redirect(request.META.get('HTTP_REFERER'))


def delete_task(request):
    if request.method == 'POST':
        pk = request.POST['id']
        if pk:
            task = Task.objects.get(id=pk)
            if task:
                task.delete()

    return redirect(request.META.get('HTTP_REFERER'))
