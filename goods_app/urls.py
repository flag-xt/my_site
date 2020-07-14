from django.urls import path

from goods_app import views

app_name='goods_app'

urlpatterns=[
    path('',views.IndexHtml.as_view(),name='index'),
    path('category/<int:categoryid>/',views.IndexHtml.as_view()),
    path('goodsdetails/<int:goodsid>/',views.DetailView.as_view()),
    path('query/',views.Query.as_view()),
]