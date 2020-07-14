import uuid

import datetime
import jsonpickle
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from cart_app.cartmanager import DBCartManger
from goods_app.models import Inventory
from pay_app.models import Order, OrderItem
from net_app.models import Address
from utils.alipay_p3 import AliPay



def toOrderView(request):

    cartitems = request.GET.get('cartitems','')
    # 获取支付总金额
    totalPrice = request.GET.get('totalPrice','')

    #判断当前用户是否登录
    if not request.session.get('user',''):
        # return HttpResponseRedirect('/user/login/?reflag=order&cartitems='+cartitems)
        return render(request,'net_app/login.html',{'reflag':'order','cartitems':cartitems,'totalPrice':totalPrice})


    #反序列化cartitems
    #[{'goodsid':1,'sizeid':'2','colorid':'3'},{}]
    cartitemList = jsonpickle.loads(cartitems)


    #获取默认收货地址
    user = jsonpickle.loads(request.session.get('user',''))
    addrObj = user.address.get(isdefault=True)

    #获取订单内容
    #[CartItem(),CartItem()]
    cartItemObjList = [DBCartManger(user).get_cartitems(**item) for item in cartitemList if item]

    # toPrice = 0
    # for ci in cartItemObjList:
    #     toPrice += ci.getTotalPrice()


    return render(request,'pay_app/order.html',{'addrObj':addrObj,'cartItemObjList':cartItemObjList,'totalPrice':totalPrice})

alipayObj = AliPay(appid='2016102500756428', app_notify_url='http://127.0.0.1:8000/pay/checkPay/', app_private_key_path='pay_app/keys/my_private_key.txt',
                 alipay_public_key_path='pay_app/keys/alipay_public_key.txt', return_url='http://127.0.0.1:8000/pay/modifycart/', debug=True)



def toPayView(request):
    addrid = request.GET.get('address', -1)
    payway = request.GET.get('payway', 'alipay')
    cartitems = request.GET.get('cartitems', '')

    params = {
        'out_trade_num': uuid.uuid4().hex,
        'order_num': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        'address': Address.objects.get(id=addrid),
        'user': jsonpickle.loads(request.session.get('user', '')),
        'payway': payway
    }

    orderObj = Order.objects.create(**params)

    # '['{'goodsid:1','sizeid:'2',...'}']'
    if cartitems:
        # [{dict1},{dict2}]
        cartitems = jsonpickle.loads(cartitems)

        orderItemList = [OrderItem.objects.create(order=orderObj, **ci) for ci in cartitems if ci]

    urlparam = alipayObj.direct_pay(subject='京东商城', out_trade_no=orderObj.out_trade_num,
                                    total_amount=request.GET.get('totalPrice', 0))

    url = alipayObj.gateway + '?' + urlparam

    return HttpResponseRedirect(url)

def modify_cart(request):
    params = request.GET.dict()
    user = jsonpickle.loads(request.session.get('user', ''))

    # 修改订单状态
    orderObj = Order.objects.get(out_trade_num=params.get('out_trade_no', ''))
    orderObj.trade_no = params.get('trade_no', '')
    orderObj.status = '待发货'
    orderObj.save()

    # 修改库存
    orderItemList = orderObj.orderitem_set.all()
    [Inventory.objects.filter(goods_id=oi.goodsid, color_id=oi.colorid, size_id=oi.sizeid).update(
        count=F('count') - oi.count) for oi in orderItemList if oi]

    # 更新购物车表中数据
    [user.cartitem_set.filter(goodsid=oi.goodsid, colorid=oi.colorid, sizeid=oi.sizeid, count=oi.count).delete() for oi
     in orderItemList if oi]

    # 更新订单表中数据

    [user.orderitem_set.create(goodsid=oi.goodsid, colorid=oi.colorid, sizeid=oi.sizeid,count=oi.count,
                               aname=Address.objects.get(id=Order.objects.get(id=oi.order_id).address_id).aname,
                               aphone=Address.objects.get(id=Order.objects.get(id=oi.order_id).address_id).aphone,
                               addr=Address.objects.get(id=Order.objects.get(id=oi.order_id).address_id).addr
                               ) for oi in orderItemList if oi]

    return HttpResponseRedirect('/order/queryAll/')

def checkPayView(request):
    # 获取所有的请求参数
    params = request.GET.dict()
    # 获取sign的值
    sign = params.pop('sign')


    # 校验是否支付成功
    if alipayObj.verify(params, sign):

        return HttpResponse('支付成功！')

    return HttpResponse('支付失败！')