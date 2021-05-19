from django.urls import path
from . import views
# . means from same folder. from (same folder) import views.



urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('aboutus/', views.aboutus, name="aboutus"),

    path('cart/',views.cart, name="cart"),
    path('add-to-cart/',views.add_to_cart, name="add_to_cart"),
    path('update-item/<str:pk>',views.update_item, name="update_item"),

    path('register/', views.register, name="register"),
    path('login/',views.login_page, name="login"),
    path('logout/',views.logout_page, name="logout"),
]
