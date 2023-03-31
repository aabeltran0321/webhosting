"""tcu_reco_system URL Configuration

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from programs.views import MyViews
from programs.views_cap import MyViews_cap


MyViews1 = MyViews()
MyViews2 = MyViews_cap()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', MyViews1.home),
    path('intro/', MyViews1.intro),
    path('geninfo/', MyViews1.gen_info),
    path('science/', MyViews1.science),
    path('numerical_reasoning/', MyViews1.numerical_reasoning),
    path('verbal_reasoning/', MyViews1.verbal_reasoning),
    path('abstract_reasoning/', MyViews1.abstract_reasoning),
    path('results/', MyViews1.results),
    path('OJMyqEABC0/', MyViews1.admin_login),
    path('adminhome/', MyViews1.admin_home),
    path('index/', MyViews2.home),
    path('sectors/', MyViews2.sectors),
    path('forecast/', MyViews2.forecast),
    path('contact/', MyViews2.contact),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

