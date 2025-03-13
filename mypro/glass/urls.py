from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('adminin', views.adminin, name='adminin'),
    path('adminup', views.adminup, name='adminup'),
    path('adminadd', views.adminadd, name='adminadd'),
    path('admin_logout_view', views.admin_logout_view, name='admin_logout_view'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)