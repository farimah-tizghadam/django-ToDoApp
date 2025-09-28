from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView,UpdateView,DeleteView)
from .models import Task
from accounts.models import Profile
from .forms import TaskForm
from django.views import View
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "todo/list_task.html"

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        tasks = Task.objects.filter(user=profile)
        return tasks

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    success_url = '/'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.user = profile
        return super(TaskCreateView, self).form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response({'form': form})

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    form_class = TaskForm
    success_url = '/'
    template_name = "todo/update_task.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user.user != self.request.user:  # Enforce that only the creator can edit
            raise PermissionDenied("You don't have permission to edit this task.")
        return obj


class TaskCompleteView(LoginRequiredMixin,View):
    model = Task
    success_url = '/'

    def get(self,request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('pk'))
        if task.user.user != self.request.user:  # Enforce that only the creator can complete task
            raise PermissionDenied("You don't have permission to edit this task.")
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
        if self.object.user.user != self.request.user:  # Enforce that only the creator can edit
            raise PermissionDenied("You don't have permission to edit this task.")
        self.object.delete()
        return redirect(self.success_url)
    

class TaskUnDoneView(LoginRequiredMixin,View):
    model = Task
    success_url = '/'

    def get(self,request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('pk'))
        task.complete = False
        task.save()
        return redirect(self.success_url) 
       