from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path("", views.signin, name="home"),
    path('university/', views.university, name="university"),
    path('university/titles_by_uni', views.titles_by_uni, name="universitytitles"),
    path('authors/',views.authors,name="authors"),
    path('abc/',views.abc,name="abc"),
    path('abc/titles_by_uni',views.titles_by_uni,name="titlesabc"),
    path('titles',views.titles_by_uni,name="titles_by_uni"),
    path('authorpubs', views.index, name="authorpubs")
]