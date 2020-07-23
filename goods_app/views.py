from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from goods_app.models import Category, Goods
from my_site import settings


def get_page_range(page,max_page,num=10):
    min=page-int(num/2)
    min=min if min>1 else 1
    max=min+num-1
    max=max if max<max_page else max_page
    return range(min,max+1)

class IndexHtml(View):
    def get(self,request,categoryid=2):
        categoryid=int(categoryid)

        categoryList=Category.objects.all().order_by('id')

        goodsList=Goods.objects.filter(category_id=categoryid)

        page=request.GET.get('page')

        paginator=Paginator(goodsList,settings.PER_PAGE_NUMBLE)

        goods_page=paginator.get_page(page)

        return render(request,'goods_app/index.html',{'categoryList':categoryList,'goodsList':goodsList,'currentid':categoryid,
                                                      'goods_page':goods_page,'page_range':get_page_range(
                                                                                            goods_page.number,paginator.num_pages,
                                                                                            settings.PAGINATOR_MAX_NUM

            )})

def recommoned(func):
    def _wrapper(detailView,request,goodsid,*args,**kwargs):

        c_goodsid=request.COOKIES.get('c_goodsid','')
        lis=[]
        goodsIdList=[id for id in c_goodsid.split() if id.strip()]

        for i in goodsIdList:
            if i not in lis:
                lis.append(i)
        goodsIdList=lis

        for i in goodsIdList:
            if int(i)>22:
                goodsIdList.remove(i)

        goodsObjList = [Goods.objects.get(id=gid) for gid in goodsIdList if int(gid) != goodsid and Goods.objects.get(id=gid).category_id == Goods.objects.get(id=goodsid).category_id][:4]

        if goodsid in goodsIdList:
            goodsIdList.remove(goodsid)
            goodsIdList.insert(0, goodsid)
        else:
            goodsIdList.insert(0, goodsid)

        response = func(detailView, request, goodsid, recommend_list=goodsObjList, *args, **kwargs)

        # 将用户访问过的商品ID列表存放至cookie中
        response.set_cookie('c_goodsid', ' '.join([str(i) for i in goodsIdList]), max_age=3 * 24 * 60 * 60)

        return response

    return _wrapper



class DetailView(View):
    @recommoned
    def get(self,request,goodsid,recommend_list=[]):
        goodsid=int(goodsid)

        try:
            goods = Goods.objects.get(id=goodsid)
            return render(request, 'goods_app/detail.html', {'goods': goods, 'recommend_list': recommend_list})

        except Goods.DoesNotExist:
            return HttpResponse(status=404)


class Query(View):
    def get(self,reuqest,categoryid=2):
        query=reuqest.session.get('query')
        categoryid = int(categoryid)

        categoryList = Category.objects.all().order_by('id')
        if query:

            goodsList = Goods.objects.filter(gname__contains=query)

            page = reuqest.GET.get('page')

            paginator = Paginator(goodsList, settings.PER_PAGE_NUMBLE)

            goods_page = paginator.get_page(page)

            return render(reuqest, 'goods_app/query.html',
                          {'categoryList': categoryList, 'goodsList': goodsList, 'currentid': categoryid,
                           'goods_page': goods_page, 'page_range': get_page_range(
                              goods_page.number, paginator.num_pages,
                              settings.PAGINATOR_MAX_NUM

                          )})
        else:
            return render(reuqest,'goods_app/query.html',{'categoryList': categoryList})

    def post(self,reuqest,categoryid=2):
        query = reuqest.POST.get('query')
        reuqest.session['query']=query
        return HttpResponseRedirect('/query/')




