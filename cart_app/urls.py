from django.urls import path

from cart_app import views

app_name='cart_app'

urlpatterns=[
    path('',views.CartView.as_view()),
    path('queryAll/',views.CartListView.as_view()),
]