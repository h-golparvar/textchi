from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name='home'),
    path('management/', include('management.urls')),
    path('blog/', include('blog.urls'), name='blog'),
]