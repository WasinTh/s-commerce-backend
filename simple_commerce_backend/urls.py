from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema')),
    path('api/admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/catalog/', include('catalog.urls')),
    path('api/sale/', include('sale.urls')),
    path('', include('mcp_server.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [path('api/silk/', include('silk.urls', namespace='silk'))]
