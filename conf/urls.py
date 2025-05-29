from django.contrib import admin
from django.urls import path, include
from core.homepage.views import IndexView
from core.login.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', include('core.login.urls')),
    path('admin/', admin.site.urls),
    path('erp/', include('core.erp.urls')),
    path('reports/', include('core.reports.urls')),
    path('user/', include('core.user.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
