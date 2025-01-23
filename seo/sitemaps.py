from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# from blog.models import Post



# class PostSitemap(Sitemap):
#     changefreq = 'daily'
#     priority = 0.7
    
#     def items(self):
#         return Post.objects.published()


#     def lastmod(self, obj):
#         return obj.updated




# For static view
class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['pages:home_page', 'pages:about_page', 'pages:contact_page',
            'pages:terms_page']  # URLs for static pages

    def location(self, item):
        return reverse(item)