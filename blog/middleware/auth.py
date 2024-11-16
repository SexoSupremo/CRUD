from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class AuthMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.PUBLIC_PATHS = [
            reverse('accounts:login'),
            reverse('accounts:signup'),
            reverse('accounts:logout'),
            '/static/',
            '/media/',
            '/favicon.ico',
        ]
        # Rutas adicionales que pueden ser configuradas en settings.py
        self.PUBLIC_PATHS.extend(getattr(settings, 'PUBLIC_PATHS', []))

    def is_public_path(self, path):
        """Verifica si la ruta es pública"""
        return any(path.startswith(public_path) for public_path in self.PUBLIC_PATHS)

    def process_request(self, request):
        """Procesa la solicitud antes de llegar a la vista"""
        if not request.user.is_authenticated:
            if not self.is_public_path(request.path):
                next_url = request.path
                login_url = f"{reverse('accounts:login')}?next={next_url}"
                return HttpResponseRedirect(login_url)
        return None

    def process_response(self, request, response):
        """Procesa la respuesta después de la vista"""
        if not request.user.is_authenticated:
            if not self.is_public_path(request.path):
                if response.status_code == 200:
                    return HttpResponseRedirect(reverse('accounts:login'))
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Procesa la vista antes de su ejecución"""
        # Obtener el nombre de la vista si está disponible
        view_name = getattr(view_func, '__name__', '')
        
        # Permitir acceso a la documentación del API si está habilitada
        if view_name.startswith('swagger') or view_name.startswith('redoc'):
            return None
            
        # Verificar si es una vista de administración
        if request.path.startswith('/admin/'):
            if not request.user.is_staff:
                return HttpResponseRedirect(reverse('accounts:login'))
            return None

        return None