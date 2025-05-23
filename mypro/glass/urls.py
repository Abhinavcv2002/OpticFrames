from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('men', views.men, name='men'),
    path('women', views.women, name='women'),

    path('userin', views.userin, name='userin'),
    path('userup', views.userup, name='userup'),
    path('signout',views.signout,name='signout'),
    path('cart/<int:product_id>/', views.cart, name='cart'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product_details/<int:pk>/', views.product_details, name='product_details'),
    path('lenses_page',views.lenses_page, name='lenses_page'),
    path('about', views.about, name='about'),
    path('Profile', views.Profile, name='Profile'),


    path('#',views.adminhome, name='adminhome'),
    path('#1', views.adminadd, name='adminadd'),
    path('admin_logout_view', views.admin_logout_view, name='admin_logout_view'),
    path('checkout',views.checkout,name='checkout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)