"""djdeneme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from blogmy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("posts/", include("blogmy.urls")),
    path("auths/", include("auths.urls")),
    path("following/", include("following.urls")),
    path('iletisim/', views.iletisim, name="iletisim"),
    path('deneme/', views.deneme, name='deneme'),
    path('deneme-ajax/', views.deneme_ajax, name='denemeajax'),
    path('deneme-ajax-2/', views.deneme_ajax2, name='denemeajax2'),
    path('mylist/', views.mylist, name='mylist'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
