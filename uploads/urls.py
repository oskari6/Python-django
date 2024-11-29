"""
URL configuration for uploads project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from uploads import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from drinks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', views.movies),
    path('movies/<int:movie_id>', views.movie),
    path('movies/upload', views.upload, name='upload'),
    path('movies/add', views.add),
    path('movies/delete/<int:id>', views.delete),
    path('', views.home, name='home'),
    path("drinks/", views.drinks),
    path('drink_list/', views.drink_list),
    path("drinks/<str:name>", views.drink),
    path('drinks/<int:id>', views.drink_detail)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
