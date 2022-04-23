from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('settings/', include('settings.urls')),
    path('staff/', include('staff.urls')),
    path('inventory/', include('inventory.urls')),
    path('customer/', include('customer.urls')),
    path('sales/', include('sales.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)