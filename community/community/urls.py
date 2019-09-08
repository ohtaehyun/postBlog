
from django.contrib import admin
from django.conf.urls import handler404
from django.urls import path, include
from comuUser import views as comuViews
from board import views as boardViews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("board.urls", namespace='key')),
    path('comuUser/', include("comuUser.urls")),
    path('catchmind/', include('consumer.urls'))
]
