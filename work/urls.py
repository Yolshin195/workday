from django.urls import path

from .views import list_work_day, create_task, begin_task, end_task, delete_task, begin_workday, end_workday
from .views import CurrentWorkDayView

urlpatterns = [
    path('', CurrentWorkDayView.as_view(), name="current_workday"),
    path('<int:year>/<int:month>/<int:day>', CurrentWorkDayView.as_view(), name="workday"),
    path('list/', list_work_day, name="list_work_day"),
    path('workday/begin', begin_workday, name="begin_workday"),
    path('workday/end', end_workday, name="end_workday"),
    path('task/create', create_task, name="create_task"),
    path('task/begin', begin_task, name="begin_task"),
    path('task/end', end_task, name="end_task"),
    path('task/delete', delete_task, name="delete_task"),
]
