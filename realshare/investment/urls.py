from django.urls import path
from . import views
from .views import login_view, register_view, home_view, seller_dashboard
urlpatterns =[
    path('admin/', admin.site.urls)
    path('', views.login_view, name='login'),
    path('search/', views.search, name='search'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('login/', views.login_view, name='login'),
    path('add-property/', views.add_property, name='add_property'),
    path('superuser-dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
    path('approve-property/<int:property_id>/', views.approve_property, name='approve_property'),
    ]