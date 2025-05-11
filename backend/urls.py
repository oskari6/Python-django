from django.contrib import admin
from django.urls import path
from uploads import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('movies/', views.movies),
    path('movies/<int:movie_id>', views.movie),
    path('movies/add/', views.add, name="add_movie"),
    path('movies/delete/<int:movie_id>', views.delete),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
