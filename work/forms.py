from datetime import datetime, UTC
from .models import Workday, Task


class TaskForm:
    def __init__(self, request):
        self.request = request

        if request.method == 'POST':
            workday_id = request.POST['workday']
            title = request.POST['title']
            begin_time_str = request.POST['begin']
            end_time_str = request.POST['end']
            description = request.POST['description']

            workday = Workday.objects.get(id=workday_id)

            begin = self.get_datetime(begin_time_str)
            end = self.get_datetime(end_time_str)

            task = Task(workday=workday, title=title, begin=begin, end=end, description=description)
            task.save()

    @staticmethod
    def get_datetime(time_str):
        if not time_str:
            return None

        hour, minute = time_str.split(':')
        datetime_now = datetime.now(UTC)
        return datetime(datetime_now.year, datetime_now.month, datetime_now.day, int(hour), int(minute), tzinfo=UTC)
