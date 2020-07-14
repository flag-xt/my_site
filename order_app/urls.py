from django.urls import path

from order_app import views

app_name='order_app'

urlpatterns=[
    path('',views.OrderView.as_view()),
    path('queryAll/',views.OrderListView.as_view()),
]