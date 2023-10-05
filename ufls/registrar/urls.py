from django.urls import include, path
from registrar import views
urlpatterns = [
    path('',views.regForm1,name="Registration Form"),
    path('api/create',views.createReg1,name="Registration Form Handle"),
    path('api/cartContents',views.cartContents,name="Cart contents HTML"),
    path('api/cartContentsHTML',views.cartContentsHTML,name="Cart Contents HTML"),
    path('api/remCart/<str:itm>',views.removeFromCart,name="Remove Registrant from Cart"),
    path('api/webhooks/stripe',views.stripe_webhook,name="Registration Form Webhooks"),
    path('checkout',views.checkout,name="Registration Checkout Screen"),
    path('checkout/exec',views.checkoutExec,name="Registration Checkout Execute"),
    path('success',views.success,name="Registration Success!"),
]
