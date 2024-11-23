from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProductsView.as_view(), name="products"),
    path("product/<int:product_id>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("categories/", views.CategoryView.as_view(), name="categories"),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('change-cart-product-quantity/<int:cart_product_id>/<str:action>/', views.change_cart_product_quantity, name='change_cart_product_quantity'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('product-search', views.product_search, name='product_search')
]