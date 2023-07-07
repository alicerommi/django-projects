from django.contrib import admin
from django.urls import path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name="login"),
    path('login_form', views.sign_in, name='sign_in'),
    path('home', views.home, name='home'),
]
