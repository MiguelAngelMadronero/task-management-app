"""Core Urls."""
from django.urls import path
from webtask import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('projects/',
         views.ProjectListView.as_view(), name='projects'),
    path('projects/new/',
         views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/edit/',
         views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/',
         views.ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/<int:project_id>/tasks/',
         views.TaskListView.as_view(), name='tasks'),
    path('projects/<int:project_id>/tasks/new/',
         views.TaskCreateView.as_view(), name='task_create'),
    path('projects/<int:project_id>/tasks/<int:pk>/edit/',
         views.TaskUpdateView.as_view(), name='task_edit'),
    path('projects/<int:project_id>/tasks/<int:pk>/delete/',
         views.TaskDeleteView.as_view(), name='task_delete'),
    path('projects/<int:project_id>/tasks/<int:pk>/detail/',
         views.TaskDetailView.as_view(), name='task_detail'),
    path('projects/<int:project_id>/tasks/<int:pk>/status/<str:new_status>/',
         views.TaskChangeStatusView.as_view(),
         name='task_change_status'),
]
