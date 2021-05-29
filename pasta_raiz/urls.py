
from django.contrib import admin
from django.urls import path, include
#uso das imagens
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('usuarios.urls')),
    path('produtos/', include('produtos.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
