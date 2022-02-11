from django.contrib import admin
from django.urls import path

from Account.views import register_view, login_view, logout_view
from PriceTracker.views import home, url_to_track, track, items, deleteItem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('url/', url_to_track, name="urlToTrack"),
    path('track/', track, name="track"),
    path('items/', items, name="items"),
    path('items/deleteItem', deleteItem, name="deleteItem"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]
