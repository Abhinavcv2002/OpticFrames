from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('eyeglass', views.eyeglass, name='eyeglass'),
    path('sunglass', views.sunglass, name='sunglass'),

    path('userin', views.userin, name='userin'),
    path('userup', views.userup, name='userup'),
    path('user_logout_view', views.user_logout_view, name='user_logout_view'),
    path('cart', views.cart, name='cart'),
    path('product_details', views.product_details, name='product_details'),

    path('home',views.home, name='home'),
    path('sellerin', views.sellerin, name='sellerin'),
    path('sellerup', views.sellerup, name='sellerup'),
    path('selleradd', views.selleradd, name='selleradd'),
    path('seller_logout_view', views.seller_logout_view, name='seller_logout_view'),

]