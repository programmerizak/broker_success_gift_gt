"""
URL configuration for website project.

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
from django.urls import path,include
# from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

############### SITEMAP #################################
from django.contrib.sitemaps.views import sitemap
from seo.sitemaps import StaticViewSitemap



admin.site.site_header = " TRADE XSPHERE "
admin.site.site_title = "TRADE XSPHERE  ADMIN PORTAL"
admin.site.index_title = "WELCOME TO TRADE XSPHERE PORTAL"



sitemaps = {
    'static': StaticViewSitemap,
    # 'post': PostSitemap,
}


urlpatterns = [
    path('secure/confidential/', admin.site.urls),
    path('wp-admin/', include('admin_honeypot.urls')),
    path('', include('pages.urls', namespace='pages')),
    path('auth/', include('allauth.urls')),
    path('user/', include('users.urls',namespace='users')),
    ###################################################################
    path('trade/', include('trade.urls',namespace='trade')),
    # path('plan/', include('plan.urls',namespace='plans')),
    path('wallet/', include('wallet.urls', namespace='wallet')),
    path('launchpad/', include('launchpad.urls', namespace='launchpad')),
    path('stake/', include('stake.urls', namespace='stake')),
    path('copy-trader/', include('copy_trader.urls', namespace='copy_trader')),
    path('kyc/', include('kyc.urls', namespace='kyc')),
    ############## SEO ########################################
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    # path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps},
    #      name='django.contrib.sitemaps.views.sitemap'),
    # #############################################################################
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

]

urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

### If Debug is True
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


