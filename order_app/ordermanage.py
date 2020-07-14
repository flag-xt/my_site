import jsonpickle
from django.db.models import F

from order_app.models import OrderItem


class OrderManager(object):
    def add(self,goodsid,colorid,sizeid,count,*args,**kwargs):
        '''添加商品，如果商品已经存在就更新商品的数量(self.update())，否则直接放到购物车'''
        pass

    def delete(self,goodsid,colorid,sizeid,*args,**kwargs):
        '''删除一个购物项'''
        pass

    def update(self,goodsid,colorid,sizeid,count,step,*args,**kwargs):
        '''更新购物项的数据,添加减少购物项数据'''
        pass

    def queryAll(self,*args,**kwargs):
        ''':return OrderItem  多个购物项'''
        pass


class DBCartManger(OrderManager):
    def __init__(self,user):
        self.user = user

    def add(self,goodsid,colorid,sizeid,count,*args,**kwargs):


        if self.user.orderitem_set.filter(goodsid=goodsid,colorid=colorid,sizeid=sizeid).count()==1:

            self.update(goodsid,colorid,sizeid,count,*args,**kwargs)
        else:
            OrderItem.objects.create(goodsid=goodsid,colorid=colorid,sizeid=sizeid,count=count,user=self.user)



    def delete(self,goodsid,colorid,sizeid,*args,**kwargs):
        self.user.orderitem_set.filter(goodsid=goodsid,colorid=colorid,sizeid=sizeid).update(count=0,isdelete=True)


    def update(self,goodsid,colorid,sizeid,step,*args,**kwargs):

        self.user.orderitem_set.filter(goodsid=goodsid,colorid=colorid,sizeid=sizeid).update(count=F('count')+int(step),isdelete=False)

    def queryAll(self,*args,**kwargs):

        return self.user.orderitem_set.order_by('id').filter(isdelete=False).all()



    #获取当前用户下的所有购物项
    def get_orderitems(self,goodsid,sizeid,colorid,*args,**kwargs):
        return self.user.orderitem_set.get(goodsid=goodsid,sizeid=sizeid,colorid=colorid)



# 工厂方法
#根据当前用户是否登录返回相应的CartManger对象
def getOrderManger(request):
    if request.session.get('user'):
        #当前用户已登录
        return DBCartManger(jsonpickle.loads(request.session.get('user')))
