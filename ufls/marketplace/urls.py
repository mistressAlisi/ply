from django.urls import path,include
from marketplace import views

app_name="marketplace"

urlpatterns = [
	#path('captcha/', views.captcha, name='new'),
	#path('new/', views.new, name='new-form'),
	#path('area-selection/', views.areaSelect, name='area-select'),
	#path('application/', views.application, name='application'),
	#path('application/<str:selectedArea>/', views.application, name='application-selected'),
	#path('alley/application/', views.artistsAlleyApp, name='aa-application'),
	#path('alley/application/done/', views.artistsAlleyAppDone, name='aa-done'),
	#path('edit/application/update/', views.applicationUpdate, name='application-update'),
	#path('verify/', views.verify, name='verify'),
	#path('pay/', views.pay, name='pay'),
	#path('codes/', views.codes, name='codes'),
	#path('book/', views.book, name='book'),
	#path('invoices/', views.invoices, name='invoices'),
	path('sign-generate/', views.signGenerate, name='sign-generate'),
	path('sign/finish/<str:pk>/', views.signFinish, name='sign-finish'),
	path('invoice/order-confirm/', views.orderConfirm, name='order-confirm'),
	path('square/order-confirm/', views.orderConfirm, name='order-confirm-s'),
	#path('invoice/<str:pk>/', views.invoice, name='invoice'),
	#path('invoice/<str:pk>/square/', views.invoiceSquare, name='invoice-square'),
	path('invoice/<str:pk>/square/data/', views.invoiceSquareData, name='invoice-square-data'),
	path('send/', views.sendOverToDealers, name='send-over-to-dealers'),
	#path('dealer/assistants/', views.assistantDashboard, name='assistant-dashboard'),
	#path('dealer/assistants/register/', views.assistantNew, name='assistant-new'),
	#path('dealer/assistants/edit/<str:pk>/', views.assistantEdit, name='assistant-edit'),
]
