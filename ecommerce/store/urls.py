from django.urls import path
from . import views
app_name="store"
urlpatterns=[
    path('',views.store_view,name="home-page"),
    path('update_item',views.update_item,name="update_item"),
    path('update_wishlist',views.update_wishlist,name="update_wishlist"),
    path('search_results',views.search_results,name="search"),
    path('cart',views.cart,name="cart"),
    path('checkout',views.checkout,name='checkout'),
    path('product/<int:id>',views.product_view,name='product'),
    path('process_order',views.processOrder,name="process-order"),
    path('help',views.customer_service,name='help'),
    path('tags/<str:cat>',views.tags,name='tags'),
]