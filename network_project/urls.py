"""
URL configuration for network_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from dashboard.views import ping_dashboard, sensor_graphs_view, login_api, add_ip_view, submit_add_ip,get_sensors_by_ip_api,sensor_csv_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ping_dashboard, name='home_dashboard'),
    path('graphs/', sensor_graphs_view, name='sensor_graphs'),
    path('login_api/', login_api, name='login_api'),
    path('add_ip/', add_ip_view, name='add_ip'),
    path('submit_add_ip/', submit_add_ip, name='submit_add_ip'),
    path('api/get_sensors_by_ip/', get_sensors_by_ip_api, name='get_sensors_by_ip'),
    path('api/sensor_csv_data/',sensor_csv_data, name='sensor_csv_data'),
]
