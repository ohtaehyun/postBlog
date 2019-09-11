from django.conf.urls import handler404
from django.urls import path, include

from . import views

app_name = "board"

urlpatterns = [
    path('', views.signIn),
    path('home', views.home),
    path('posts', views.postList.as_view(), name='key'),
    path('posts/<int:pk>', views.postList.as_view(), name='key'),
    path('post/<int:pk>', views.postDetail.as_view(), name='postId'),
    path('review', views.review),
    path('signOut', views.signOut),
    path('signIn', views.signIn),
    path('posts/addCategory', views.addCategory),
    path('posts/addPost', views.addPost),
    # path('trolo', views.trolo),
    path('troloTest', views.troloTest)
]
# handler404 = views.error_404
