"""
URL configuration for customers project.

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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from django.urls import path
from .views.customer_views import customers, customer
from .views.register_views import register
from .views.register_views import google_auth
from .views.employee_views import employees, employee
from .views.order_views import orders, orders_customer, order
from .views.item_views import items, item

from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema  # Assuming schema.py is in the same app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/customers/', customers, name='customers'),
    path('api/customers/<int:id>/', customer, name='customer'),
    path('api/customers/<int:customer_id>/orders/', orders_customer, name='customer_orders'),
    path('api/customers/<int:customer_id>/orders/<int:order_id>/', order, name='customer_order'),
    path('api/orders/', orders, name='orders'),
    path('api/items/', items, name='items'),
    path('api/items/<int:id>/', item, name='item'),
    path('api/register/', register, name='register'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('api/auth/google/', google_auth, name='google_auth'),
    path('api/employees/', employees, name='employees'),
    path('api/employees/<int:id>/', employee, name='employee-detail'),
]
#for serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)