from django.conf.urls import handler404
from django.urls import path, include

from . import views

app_name = "board"

urlpatterns = [
    path('', views.signIn),
    path('home', views.home),
    path('study/', views.study, name='key'),
    path('study/(?cate<int:key>)', views.getPosts, name='key'),
    path('review', views.review),
    path('signOut', views.signOut),
    path('signIn', views.signIn),
    path('study/addCategory', views.addCategory),
    path('study/addPost', views.addPost)
]
# handler404 = views.error_404
