from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Account.views import (
    register_view,
    login_view,
    logout_view,
)
from PriceTracker.views import (
    home
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
