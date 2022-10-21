from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = 'sMARKET E-commerce'
admin.site.site_title = 'sMARKET ADMIN'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketapp.urls')),
    path('sMarketauth/', include('smarketauth.urls')),
    path('sMarket/blog/', include('blog.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
