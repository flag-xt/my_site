from django.urls import path
from pay_app import views

urlpatterns=[
    path('', views.toOrderView),
    path('toPay/', views.toPayView),
    path('checkPay/', views.checkPayView),
    path('modifycart/',views.modify_cart),
]