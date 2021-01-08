from django.urls import path
from . import views
app_name="accounts"
urlpatterns = [
    path('register', views.sing_up_view, name="register"),
    path('login', views.login_view, name="login")
]
