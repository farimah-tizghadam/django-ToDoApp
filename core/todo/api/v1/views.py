from todo.models import Task
from rest_framework import viewsets
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import DefaultPagination
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['title', 'complete']
    search_fields = ["title", "complete"]
    ordering_fields = ["creation_date"]
    pagination_class = DefaultPagination
    filterset_class = TaskFilter
