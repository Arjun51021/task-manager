from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.task_list, name="task_list"),
    path("add/", views.add_task, name="add_task"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
]

