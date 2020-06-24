"""settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import sys
sys.path.append("..")
sys.path.append("..\..")
from django.contrib import admin
from django.urls import path
from app.controller.api import views as api_views
import re as r

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',api_views.index,name="index"),
    path('ImportData/',api_views.import_data,name="import_data"),
    path('DeleteData/<str:table_name>/',api_views.delete_data,name="delete_data"),
    path('SearchTable/',api_views.search_table,name="search_table"),
    path('<str:table_name>/',api_views.search_data_by_name,name="search_data_by_name"),
    path('SearchAllTable/',api_views.search_all_table,name="search_all_table"),
    path('DataDownload/',api_views.data_download,name="data_download"),
    path('Detect/',api_views.detect,name="detect"),
]
