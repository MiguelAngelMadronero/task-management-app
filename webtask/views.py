# from django import forms
from django.shortcuts import get_object_or_404, redirect, render, Http404
from django.views import View
from django.contrib.auth import login, logout
from core.models import Project, Task
from webtask import forms
from django.views.generic import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm, TaskForm
from django.db.models import Q


class Index(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        """Lógica para manejar el método GET."""
        user = request.user
        ctx = {
            'user': user,
        }
        return render(request, self.template_name, ctx)


class SignUp(FormView):
    template_name = 'signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        Se ejecuta cuando el formulario es válido.
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "¡Te has registrado exitosamente!")
        return super().form_valid(form)


class Login(View):
    """Login view."""

    form_class = forms.LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        """GET method."""
        if request.user.is_authenticated:
            return redirect('index')
        form = self.form_class()
        ctx = {
            'form': form,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        """POST method."""
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.login()
            if user:
                login(request, user)
                if request.GET:
                    url = request.GET.get('next')
                    return redirect(url)
                else:
                    return redirect('index')
        ctx = {
            'form': form,
        }
        return render(request, self.template_name, ctx)


class LogoutView(View):
    """Logout view."""

    def get(self, request, *args, **kwargs):
        """GET method."""
        logout(request)
        return redirect('login')


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user)
            | Q(tasks__assigned_to=self.request.user)).distinct()


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        # messages.success(self.request, "Proyecto creado con éxito.")
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects')

    def get_object(self, queryset=None):
        project = get_object_or_404(
            Project,
            pk=self.kwargs['pk'],
            owner=self.request.user)
        return project


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_delete.html'
    success_url = reverse_lazy('projects')

    def get_object(self, queryset=None):
        project = get_object_or_404(
            Project,
            pk=self.kwargs['pk'],
            owner=self.request.user)
        return project


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        project_id = self.kwargs['project_id']

        qs = Task.objects.filter(
            project_id=project_id).filter(
            Q(project__owner=self.request.user)
            | Q(assigned_to=self.request.user)
        )
        status_filter = self.request.GET.get('status')
        if status_filter in [
            Task.TaskStatus.PENDING,
            Task.TaskStatus.IN_PROGRESS,
            Task.TaskStatus.COMPLETED
        ]:
            qs = qs.filter(status=status_filter)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.filter(
            pk=self.kwargs['project_id']
        ).filter(
            Q(owner=self.request.user)
            | Q(tasks__assigned_to=self.request.user)
        ).distinct().first()
        if not project:
            raise Http404("No tienes permiso para ver este proyecto")
        context['project'] = project
        context['selected_status'] = self.request.GET.get('status', "")
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        queryset = super().get_queryset()
        return get_object_or_404(
            queryset.filter(
                Q(project__owner=self.request.user) |
                Q(assigned_to=self.request.user)
            ),
            pk=self.kwargs['pk'],
            project__id=self.kwargs['project_id']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def form_valid(self, form):
        project = get_object_or_404(
            Project,
            pk=self.kwargs['project_id'],
            owner=self.request.user
        )
        form.instance.project = project
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        url_success = reverse_lazy('tasks', kwargs={
            'project_id': self.kwargs['project_id']
        })
        return url_success


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'

    def get_object(self, queryset=None):
        project = get_object_or_404(
            Project,
            pk=self.kwargs['project_id'],
            owner=self.request.user
        )
        task = get_object_or_404(Task, pk=self.kwargs['pk'], project=project)
        return task

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        url_success = reverse_lazy(
            'tasks',
            kwargs={'project_id': self.kwargs['project_id']})
        return url_success


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'

    def get_object(self, queryset=None):
        project = get_object_or_404(
            Project,
            pk=self.kwargs['project_id'],
            owner=self.request.user
        )
        task = get_object_or_404(Task, pk=self.kwargs['pk'], project=project)
        return task

    def get_success_url(self):
        url_success = reverse_lazy(
            'tasks',
            kwargs={'project_id': self.kwargs['project_id']}
        )
        return url_success


class TaskChangeStatusView(LoginRequiredMixin, View):
    def get(self, request, project_id, pk, new_status):
        task = get_object_or_404(Task, pk=pk, project__id=project_id)
        if (request.user == task.project.owner or
                request.user == task.assigned_to):
            if new_status in [
                Task.TaskStatus.PENDING,
                Task.TaskStatus.IN_PROGRESS,
                Task.TaskStatus.COMPLETED
            ]:
                task.status = new_status
                task.save()
        return redirect('tasks', project_id=project_id)
