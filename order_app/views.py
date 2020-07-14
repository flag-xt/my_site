from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from order_app.ordermanage import getOrderManger

class OrderView(View):
    def post(self, request):
            request.session.modified = True
            flag = request.POST.get('flag')

            if flag == 'add':
                orderManagerObj = getOrderManger(request)
                orderManagerObj.add(**request.POST.dict())

            elif flag == 'plus':
                orderManagerObj = getOrderManger(request)
                # {'flag':'plus','goodsid':'1',...}
                orderManagerObj.update(step=1, **request.POST.dict())

            elif flag == 'minus':
                orderManagerObj = getOrderManger(request)
                # {'flag':'plus','goodsid':'1',...}
                orderManagerObj.update(step=-1, **request.POST.dict())

            elif flag == 'delete':
                orderManagerObj = getOrderManger(request)
                orderManagerObj.delete(**request.POST.dict())

            return HttpResponseRedirect('/order/queryAll/')

class OrderListView(View):
    def get(self,request):
        orderManagerObj=getOrderManger(request)
        cartItemList=orderManagerObj.queryAll()

        return render(request,'order_app/order.html',{'cartItemList':cartItemList})


