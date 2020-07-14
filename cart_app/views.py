from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart_app.cartmanager import getCartManger


class CartView(View):
    def post(self,request):
        request.session.modified=True
        flag=request.POST.get('flag')

        if flag=='add':
            cartManagerObj=getCartManger(request)
            cartManagerObj.add(**request.POST.dict())

        elif flag == 'plus':
            cartManagerObj = getCartManger(request)
            # {'flag':'plus','goodsid':'1',...}
            cartManagerObj.update(step=1, **request.POST.dict())

        elif flag == 'minus':
            cartManagerObj = getCartManger(request)
            # {'flag':'plus','goodsid':'1',...}
            cartManagerObj.update(step=-1, **request.POST.dict())

        elif flag == 'delete':
            cartManagerObj = getCartManger(request)
            cartManagerObj.delete(**request.POST.dict())

        return HttpResponseRedirect('/cart/queryAll/')


class CartListView(View):
    def get(self,request):
        cartManagerObj=getCartManger(request)
        cartItemList=cartManagerObj.queryAll()

        return render(request,'cart_app/cart.html',{'cartItemList':cartItemList})