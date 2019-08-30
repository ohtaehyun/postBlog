from django.conf.urls import handler404
from django.urls import path
from . import views
urlpatterns = [
    path('', views.signIn),
    path('home', views.home),
    path('study', views.study),
    path('review', views.review),
    path('signOut', views.signOut),
    path('signIn', views.signIn),
    path('addCategory', views.addCategory),
    path('addPost', views.addPost)
]
# handler404 = views.error_404
