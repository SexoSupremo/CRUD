from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # Rutas de autenticación
    path('signup/', views.UserCreateAndLoginView.as_view(), name='signup'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True,template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    
    # Rutas de gestión de usuario
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    
    # Rutas de gestión de contraseña
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',success_url='/accounts/password_change/done/'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    
    # Ruta de eliminación de cuenta
    path('user_delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),
    
    # Ruta de redirección después del registro exitoso
    path('registration_success/', views.RegistrationSuccess.as_view(), name='registration_success'),
]