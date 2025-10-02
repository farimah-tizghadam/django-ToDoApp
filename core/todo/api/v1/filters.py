from django_filters import rest_framework as filters
from todo.models import Task


class TaskFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="creation_date", lookup_expr='gte', label='from date')
    to_date = filters.DateFilter(field_name="creation_date", lookup_expr='lte', label='to date')

    class Meta:
        model = Task
        fields = [ 'title','updated_date', 'from_date', 'to_date']