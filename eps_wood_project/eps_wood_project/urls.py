"""
URL configuration for eps_wood_project project.

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
from django.urls import path
from eps_wood_app import views


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    # path('adm',views.adm,name='adm'),
    path('customer_register/',views.customer_register,name='customer_register'),
    path('owner_register/',views.owner_register,name='owner_register'),
    path('login/', views.login_view, name='login'),

    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('owner_dashboard/',views.owner_dashboard,name='owner_dashboard'),
    path('customer_dashboard/',views.customer_dashboard,name='customer_dashboard'),


    path('owner_profile/',views.owner_profile,name='owner_profile'),
    path('owner_update_profile/',views.owner_update_profile,name='owner_update_profile'),

    path('add_products/',views.add_products,name='add_products'),
    path('product_list/',views.product_list,name='product_list'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),

    path('customer_profile',views.customer_profile,name='customer_profile'),
    path('customer_profile_update',views.customer_profile_update,name='customer_profile_update'),
    path('products',views.products,name='products'),
    path('product_details/<int:p_id>/',views.product_details,name='product_details'),

    path('my_cart',views.my_cart,name='my_cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove_item/<int:item_id>/',views.remove_item,name='remove_item'),
    path('checkout',views.checkout,name='checkout'),
    path('place_order',views.place_order,name='place_order'),
    path('order_history',views.order_history,name='order_history'),
    path('customer_order_details/<int:item_id>/',views.customer_order_details,name='customer_order_details'),
    path('cancel_order/<int:item_id>/', views.cancel_order, name='cancel_order'),


    path('incoming_orders',views.incoming_orders,name='incoming_orders'),
    path('update_order_status/<int:item_id>/',views.update_order_status,name='update_order_status'),
    path('order_details/<int:item_id>/',views.order_details,name='order_details'),

    path('pending_owners/', views.pending_owners, name='pending_owners'),
    path('approve_owner/<int:owner_id>/', views.approve_owner, name='approve_owner'),
    path('reject_owner/<int:owner_id>/', views.reject_owner, name='reject_owner'),
    path('owner_list/', views.owner_list, name='owner_list'),


    path('customer_list/', views.customer_list, name='customer_list'),
    path('toggle_customer_status/<int:customer_id>/<str:action>/', views.toggle_customer_status, name='toggle_customer_status'),

    path('logout/',views.logout,name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
