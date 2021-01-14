from django.urls import path
from . import views
app_name="accounts"
urlpatterns = [
    path('register', views.sing_up_view, name="register"),
    path('login', views.login_view, name="login"),
    path('logout',views.logout_view,name="logout"),
    path('profile',views.profile_view,name="profile"),
    path('addproduct',views.add_product,name="Product"),
    path('edit_profile',views.edit_profile,name="edit_profile")
]
