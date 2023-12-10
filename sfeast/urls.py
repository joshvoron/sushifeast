from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers

from users.views import BasketViewSet, UpdateBasket

router = routers.DefaultRouter()
router.register(r'basket', BasketViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace='products')),
    path('', RedirectView.as_view(url='products/', permanent=True)),
    path('users/', include('users.urls', namespace='users')),
    path('api-auth/', include('rest_framework.urls')),
    path('basket/<int:pk>', UpdateBasket.as_view())
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
