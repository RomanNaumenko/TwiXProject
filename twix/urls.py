from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile-list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update/', views.update_user, name="update_user"),
]