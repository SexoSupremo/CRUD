from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'blog'

urlpatterns = [
    # Vista principal - Lista de tareas
    path('', login_required(views.index), name='index'),
    
    # Creación de nueva tarea
    path('create/', login_required(views.create), name='create'),
    
    # Detalles de tarea
    path('detail/<int:article_id>/', 
         login_required(views.detail), 
         name='detail'),
    
    # Edición de tarea
    path('edit/<int:article_id>/', 
         login_required(views.edit), 
         name='edit'),
    
    # Eliminación de tarea
    path('delete/<int:article_id>/', 
         login_required(views.delete), 
         name='delete'),
]
