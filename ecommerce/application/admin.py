from django.contrib import admin
from application.models import Product, ImageGallery, Cart, Order, OrderDetail

class ImageGalleryAdmin(admin.StackedInline):
    model = ImageGallery

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageGalleryAdmin]

@admin.register(ImageGallery)
class ImageGalleryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderDetail)
