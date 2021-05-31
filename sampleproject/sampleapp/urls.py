from django.urls import path
from . import views
# . means from same folder. from (same folder) import views.


urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('aboutus/', views.aboutus, name="aboutus"),

    path('cart/', views.cart, name="cart"),
    path('add-to-cart/', views.add_to_cart, name="add_to_cart"),
    path('update-item/<str:pk>/', views.update_item, name="update_item"),
    path('delete-item/<str:pk>/', views.delete_item, name="delete_item"),
    path('products/<str:pk>/', views.products, name="products"),

    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),

    path('purchase/', views.purchase_choice, name="purchase_choice"),
    path('purchase-step2/', views.purchase_step2, name="purchase_step2"),
]
