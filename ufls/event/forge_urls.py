from django.urls import include, path
from . import forge_views,forge_api_views
urlpatterns = [
    path('create',forge_views.create_event,name="Create Event"),
    path('table', forge_views.event_table, name="Event Table"),
    path('query', forge_views.event_query, name="Query Event"),
    path('link', forge_views.link_community, name="Event->Community Link"),
    path('modify', forge_views.event_modify, name="Modify Event"),
    path('api/create/',forge_api_views.create_event_handle,name="Create Event Handle"),
    path('api/query/<uuid:event>',forge_api_views.query_handle, name="Query Handle"),
    path('api/link/<uuid:com>',forge_api_views.link_handle, name="Community Link Handle"),
    path('api/link/create/', forge_api_views.link_create_handle, name="Community Link Create Handle"),
    path('api/modify/<uuid:event>', forge_api_views.edit_event_handle, name="Edit Event Handle"),
    # path('api/cartContents',views.cartContents,name="Cart contents HTML"),
    # path('api/cartContentsHTML',views.cartContentsHTML,name="Cart Contents HTML"),
    # path('api/remCart/<str:itm>',views.removeFromCart,name="Remove Registrant from Cart"),
    # path('api/remLoot/<str:itm>', views.removeLootFromCart, name="Remove Loot Item from Cart"),
    # path('api/webhooks/stripe',views.stripe_webhook,name="Registration Form Webhooks"),
    # path('checkout',views.checkout,name="Registration Checkout Screen"),
    # path('checkout/exec',views.checkoutExec,name="Registration Checkout Execute"),
    # path('success',views.success,name="Registration Success!"),
]
