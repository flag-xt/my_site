from django.db import models

# Create your models here.
from net_app.models import Address, User


class Order(models.Model):
    out_trade_num = models.UUIDField()
    order_num = models.CharField(max_length=50)
    trade_no = models.CharField(max_length=120,default='')
    status = models.CharField(max_length=20,default='待支付')
    payway = models.CharField(max_length=20,default='alipay')
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    user = models.ForeignKey(User,models.CASCADE)


    def __str__(self):
        return self.order_num

class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE)