from django.urls import path
from application import views

urlpatterns = [
    path('',views.index,name="index"),
    path('<id>/detail',views.detail,name="detail"),
    path('show/',views.showCart, name="showCart"),
    path('addToCart/',views.addToCart,name="addToCart"),
    path('increaseCart/',views.increaseCart,name="increaseCart"),
    path('decreaseCart/',views.decreaseCart,name="decareaseCart"),
    path('removeCart/',views.removeCart,name="removeCart"),
]