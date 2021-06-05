"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from store import urls as storeurls
from medicine import urls as medicineurls
from order import urls as orderurls
from user import urls as userurls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include(storeurls)),
    path('medicine/', include(medicineurls)),
    path('order/', include(orderurls)),
    path('user/', include(userurls)),
]
