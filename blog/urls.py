from django.urls import path
from . import views
from django.contrib import admin
app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')), 
]
