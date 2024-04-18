from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
	path('', views.index, name='index'),
	path('confirm/', views.ConfirmView.as_view(), name='confirm'),
	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('return/', views.ReturnView.as_view(), name='return'),
	path('mybooks/', views.MybooksView.as_view(), name='mybooks'),

	path('name/', views.get_name, name='name'),
	path('book/<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('reserve/<int:pk>/', views.reserve, name='reserve'),
	path('confirm/<int:pk>/', views.confirm_detail, name='confirm_detail'),
	path('checkout/<int:pk>/', views.checkout_detail, name='checkout_detail'),
	path('return/<int:pk>/', views.return_detail, name='return_detail'),
	path('status/<int:pk>/', views.status_detail, name='status_detail'),
]