from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('store.urls',namespace = 'store')),
    path('accounts/',include('accounts.urls',namespace = 'accounts')),
    path('cart',include('cart.urls', namespace='cart')),
    path('order',include('order.urls',namespace='order')),
    path('coupons',include('coupons.urls',namespace='coupons')),
    # APIS
    path('v1/api/',include('apis.urls',namespace='api')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)