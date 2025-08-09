from django.urls import path
from .views import ItemDetailView, ItemPaymentPageView, CreateItemPaymentIntentView, OrderDetailView, OrderPaymentPageView, CreateOrderPaymentIntentView

urlpatterns = [
    path('item/<int:id>/', ItemDetailView.as_view(), name='item-detail'),
    path('item/<int:id>/payment/', ItemPaymentPageView.as_view(), name='item-payment-page'),
    path('item/<int:id>/create-payment-intent/', CreateItemPaymentIntentView.as_view(), name='create-item-payment-intent'),
    path('order/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/<int:id>/payment/', OrderPaymentPageView.as_view(), name='order-payment-page'),
    path('order/<int:id>/create-payment-intent/', CreateOrderPaymentIntentView.as_view(), name='create-order-payment-intent'),
]