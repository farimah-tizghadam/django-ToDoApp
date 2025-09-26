from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,UpdateView,DeleteView)
from .models import Task
from .forms import TaskForm
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "todo/list_task.html"

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    form_class = TaskForm
    success_url = '/'
    template_name = "todo/update_task.html"


class TaskCompleteView(LoginRequiredMixin,View):
    model = Task
    success_url = '/'

    def get(self,request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('pk'))
        task.complete = True
        task.save()
        return redirect(self.success_url) 
       

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = "task"
    success_url = '/'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)