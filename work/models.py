import uuid

from django.db import models


class Workday(models.Model):
    """
    Модель для представления рабочего дня.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    day = models.DateField(unique=True)
    begin = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)

    @property
    def total_worked_hours(self) -> float:
        """
        Вычисление общего количества отработанных часов для данного Workday
        :return: float количество отработанных часов
        """
        tasks = self.task_set.all()  # Получаем все связанные задачи

        total_hours = sum((task.end - task.begin).seconds // 3600 for task in tasks if task.end and task.begin)
        return total_hours


class Task(models.Model):
    """
    Модель для представления задачи над которой вы работали.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workday = models.ForeignKey(Workday, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True)
    begin = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
