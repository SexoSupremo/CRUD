from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView  # Añadido
from . import views  # Añadido

urlpatterns = [
    path('signup/', views.UserCreateAndLoginView.as_view(), name='signup'),  # Cambiado
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='accounts/login.html'
    ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
]