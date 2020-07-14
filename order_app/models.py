from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
from goods_app.models import Color, Size, Goods
from net_app.models import User
from pay_app.models import Order


class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)
    aname = models.CharField(max_length=30)
    aphone = models.CharField(max_length=11)
    addr = models.CharField(max_length=100)
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def getColor(self):
        return Color.objects.get(id=self.colorid)

    def getSize(self):
        return Size.objects.get(id=self.sizeid)

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getTotalPrice(self):
        return int(self.getGoods().price) * int(self.count)
