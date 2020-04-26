from django.urls import path, include
# from .views import ProductList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete
from .views import ProductViewSet, OrderProductViewSet, OrderViewSet, CategoryViewSet, SubCategoryViewSet
from rest_framework.routers import DefaultRouter
from .views import add_to_cart, remove_from_cart, cart_item_count, order_summary
router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'order_product', OrderProductViewSet, basename='order_product')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory', SubCategoryViewSet, basename='subcategory')
urlpatterns = [
    path('add_to_cart/<slug>', add_to_cart),
    path('remove_from_cart/<slug>', remove_from_cart),
    path('cart_item_count/', cart_item_count),
    path('order_summary/', order_summary),
]
urlpatterns += router.urls