from django.urls import path
from . import views

app_name='net_app'

urlpatterns=[
    path('register/',views.Register.as_view(),name="register"),
    path('send_mail_vcode/', views.send_mail_vcode, name='send_mail_vcode'),
    path('validate_mail_vcode/', views.validate_mail_vcode, name='validate_mail_vcode'),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.LogOutView.as_view()),
    path('center/',views.centerfunc,name="center"),
    path('loadimage/',views.loadimage,name='loadimage'),
    path('vcode/',views.vcode,name='vcode'),
    path('address/',views.AddressView.as_view()),
    path('updateDefaultAddr/', views.updateDefaultAddr),
    path('loadArea/', views.loadAreaView),

]