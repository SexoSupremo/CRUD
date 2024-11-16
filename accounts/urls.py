from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Rutas de autenticación
    path('signup/', views.UserCreateAndLoginView.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='accounts/login.html',
        success_url='/'  # Redirige a la página principal después del login
    ), name='login'),
    path('logout/', LogoutView.as_view(
        next_page='login'  # Redirige al login después del logout
    ), name='logout'),

    # Rutas de gestión de usuario
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    
    # Rutas de gestión de contraseña
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), 
         name='password_change_done'),
    
    # Ruta de eliminación de cuenta
    path('user_delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),
    
    # Ruta de redirección después del registro exitoso
    path('registration_success/', views.RegistrationSuccess.as_view(), name='registration_success'),
]