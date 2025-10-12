from django.urls import path, include
from . import views

app_name = 'task'

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("create/", views.TaskCreateView.as_view(), name="create_task"),
    path("update/<int:pk>/", views.TaskUpdateView.as_view(), name="update_task"),
    path("complete/<int:pk>/", views.TaskCompleteView.as_view(), name="complete_task"),
    path("delete/<int:pk>/", views.TaskDeleteView.as_view(), name="delete_task"),
    path("undone/<int:pk>/", views.TaskUnDoneView.as_view(), name="undone_task"),
    path('api/v1/', include('todo.api.v1.urls')),
]