from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include
from creator import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='schemas')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'schemas/', views.SchemaListView.as_view(), name='schemas'),
    path(r'schemas/create/', views.SchemaCreateView.as_view(), name='create_schema'),
    path(r'schemas/<int:id>/', views.SchemaDetailView.as_view(), name='datasets'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)