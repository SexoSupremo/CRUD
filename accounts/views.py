from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib import messages
from .forms import CustomUserCreationForm, UserUpdateForm

User = get_user_model()

class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return super().handle_no_permission()

class RegistrationSuccess(TemplateView):
    template_name = 'accounts/registration_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro Exitoso'
        return context

class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:registration_success")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            email = form.cleaned_data.get("email")
            raw_pw = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=raw_pw)
            if user is not None:
                login(self.request, user)
                messages.success(self.request, "Registro exitoso.")
                return response
        except Exception as e:
            messages.error(self.request, "Error en el registro. Por favor, intente nuevamente.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrija los errores en el formulario.")
        return super().form_invalid(form)

class UserDetail(LoginRequiredMixin, OnlyYouMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = self.request.user.pk == self.get_object().pk
        return context

class UserUpdate(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_edit.html'

    def get_success_url(self):
        messages.success(self.request, "Información actualizada exitosamente.")
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrija los errores en el formulario.")
        return super().form_invalid(form)

class UserDelete(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    model = User
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Cuenta eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Por favor corrija los errores en el formulario.")
        return super().form_invalid(form)

class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/user_detail.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.user.pk})