from django.contrib import admin
from django.urls import path

from Account.views import register_view, login_view, logout_view
from PriceTracker.views import home, url_to_track, track, items

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('url/', url_to_track, name="urlToTrack"),
    path('track/', track, name="track"),
    path('items/', items, name="items"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="register"),
    path('logout/', logout_view, name="register"),
]
