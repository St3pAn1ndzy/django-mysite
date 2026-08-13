from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap

from shopapp.models import Product


class ShopSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Product.objects.filter(archived=False).all()

    def lastmod(self, obj):
        return obj.created_at
