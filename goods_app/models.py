from django.db import models

# Create your models here.

class Category(models.Model):
    cname=models.CharField(max_length=10)

    def __str__(self):
        return self.cname

class Goods(models.Model):
    gname=models.CharField(max_length=100,verbose_name='商品名称')
    gdesc=models.CharField(max_length=100,verbose_name='商品描述')
    oldprice=models.DecimalField(verbose_name='原价',max_digits=5,decimal_places=2)
    price=models.DecimalField(verbose_name='现价',max_digits=5,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='类别ID')

    def __str__(self):
        return self.gname

    def getImgUrl(self):
        return self.inventory.first().color.colorurl

    def getColors(self):
        colors = []

        for inventory in self.inventory.all():
            color = inventory.color
            if color not in colors:
                colors.append(color)

        return colors

    def getSizes(self):
        sizes = []

        for inventory in self.inventory.all():
            size = inventory.size
            if size not in sizes:
                sizes.append(size)

        return sizes

    def getDetailImagUrl(self):
        imgurls=[]
        for imgurl in self.goodsdetail.all():
            if str(imgurl.gdurl).endswith('.jpg'):
                imgurls.append(imgurl.gdurl)
        return imgurls

class GoodsDetailName(models.Model):
    gdname=models.CharField(verbose_name='商品详情',max_length=30)

    def __str__(self):
        return self.gdname

class GoodsDetail(models.Model):
    gdurl=models.ImageField(verbose_name='详情图地址',upload_to='')
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,related_name='goodsdetail')
    detailname=models.ForeignKey(GoodsDetailName,on_delete=models.CASCADE)

    def __str__(self):
        return self.detailname.gdname

class Size(models.Model):
    sname=models.CharField(verbose_name='尺寸名称',max_length=10)

    def __str__(self):
        return self.sname

class Color(models.Model):
    colorname=models.CharField(verbose_name='颜色名称',max_length=10)
    colorurl=models.ImageField(verbose_name='颜色图片地址',upload_to='color/')

    def __str__(self):
        return self.colorname

class Inventory(models.Model):
    count=models.PositiveIntegerField(verbose_name='库存数量')
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,related_name='inventory')
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
