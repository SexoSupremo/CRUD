from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')), 
]
