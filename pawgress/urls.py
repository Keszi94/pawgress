"""
URL configuration for pawgress project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('courses/', include('courses.urls')),
    path('bundles/', include('bundles.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('profiles/', include('profiles.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
