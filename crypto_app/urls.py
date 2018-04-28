from django.urls import path, include
from .views import BaseIndexView, AdminView, UserView
from django.contrib.auth.views import logout

urlpatterns = [
    path('', BaseIndexView.as_view(), name="index"),
    path('admin-view/', AdminView.as_view(), name="admin-view"),
    path('user-view/', UserView.as_view(), name="user-view"),
    path('logout/', logout, name="logout",  kwargs={'next_page': '/'}),
]