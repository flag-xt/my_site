import time

import jsonpickle
from django.core.serializers import serialize
from django.views import View

from cart_app.cartmanager import SessionCartManager
from my_site import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from io import BytesIO
# Create your views here.
from net_app.common.captcha_image import random_vcode
from net_app.common.mail_helper import send_vcode
from net_app.models import User, Area, Address


class Register(View):
    def get(self,request):
        return render(request,'net_app/register.html')

    def post(self,request):
        uname=request.POST.get("reg_userid")
        pwd=request.POST.get("reg_passwd")
        try:
            user=User.objects.get(username=uname,password=pwd)
            if user:
                return render(request,'net_app/register.html',{'msg':'用户已存在'})
        except:
            User.objects.create(username=uname,password=pwd)
            return render(request,"net_app/center.html")


def send_mail_vcode(request):
    username = request.POST.get('username')
    mail_vcode_time = request.session.get('mail_vcode_time')
    now_time = time.time()

    if mail_vcode_time and now_time < mail_vcode_time + settings.MAIL_INTERVAL:
        return JsonResponse({'msg': f'{settings.MAIL_INTERVAL}秒之内，不能重复发送邮件'})
    else:
        vcode = send_vcode(settings.MAIL_SMTP_SERVER,
                   settings.MAIL_FROM_ADDR,
                   settings.MAIL_PASSWORD,
                   username)

        request.session['mail'] = username
        request.session['mail_vcode'] = vcode
        request.session['mail_vcode_time'] = time.time()

        return JsonResponse({'msg': '已经发送，请查阅邮箱'})

def validate_mail_vcode(request):
    mail = request.session.get('mail')
    username = request.POST.get('username')

    if mail and mail == username:
        now_time = time.time()
        vcode_time = request.session.get('mail_vcode_time')

        if vcode_time and now_time <= vcode_time + settings.MAIL_EXPIRE:
            vcode = request.POST.get('vcode')
            mail_vcode = request.session.get('mail_vcode')

            if mail_vcode and mail_vcode == vcode:
                resp = {'ok': 1, 'msg': '验证码验证正确！'}
            else:
                resp = {'ok': 0, 'msg': '验证码错误！'}
        else:
            resp = {'ok': 0, 'msg': '验证码已经过期，请重新获取！'}
    else:
        resp = {'ok': 0, 'msg': '该邮箱还没有获取验证码！'}

    return JsonResponse(resp)

class Login(View):
    def get(self,request):
        reflag=request.GET.get('reflag')
        return render(request, "net_app/login.html",{'reflag':reflag})

    def post(self,request):
        uname = request.POST.get("reg_userid")
        pwd = request.POST.get("reg_passwd")
        reflag=request.POST.get('reflag')
        user = User.objects.filter(username=uname, password=pwd)

        if user:
            request.session['user'] = jsonpickle.dumps(user[0])
            SessionCartManager(request.session).migrateSession2DB()

            if reflag == 'cart':
                return HttpResponseRedirect('/cart/queryAll/')
            return HttpResponseRedirect('/user/center/')
        return render(request,'net_app/login.html',{'msg':'用户名或密码错误'})

class LogOutView(View):
    def post(self,request):
        #清空session中的所有数据
        request.session.flush()

        #返回响应
        return JsonResponse({'logout':True})


def centerfunc(request):
    return render(request,'net_app/center.html')

def loadimage(request):
    stream=BytesIO()
    image,code=random_vcode()
    '''
    save的第二个参数不是扩展名,它是 image file formats中指定的format参数,JPEG文件的格式说明符是JPEG,而不是JPG.
    如果您希望PIL决定要保存哪种格式,则可以忽略第二个参数  image.save(name)
    '''
    image.save(stream,'JPEG')
    request.session['check_code']=code
    return HttpResponse(stream.getvalue())


def vcode(request):
    html_code=request.POST.get('vcode')
    code=request.session.get("check_code")
    if html_code and html_code==code:
        resp = {'ok': 1, 'msg': '验证码验证正确！'}
    else:
        resp = {'ok': 0, 'msg': '验证码错误！'}
    return JsonResponse(resp)


class AddressView(View):
    def get(self,request):
        userstr=request.session.get('user')
        if userstr:
            user=jsonpickle.loads(userstr)

        addr_list=user.address.all()

        return render(request,'net_app/address.html',{'addr_list':addr_list})

    def post(self,request):
        aname = request.POST.get('aname','')
        aphone=request.POST.get('aphone','')
        addr=request.POST.get('addr','')

        userstr=request.session.get('user','')
        if userstr:
            user=jsonpickle.loads(userstr)

        Address.objects.create(aname=aname, aphone=aphone, addr=addr, user=user,
                               isdefault=(lambda count: True if count == 0 else False)(user.address.count()))

        return HttpResponseRedirect('/user/address/')

def loadAreaView(request):
    pid = request.GET.get('pid', -1)
    pid = int(pid)

    areaList = Area.objects.filter(parentid=pid)

    # 序列化数据
    jareaList = serialize('json', areaList)

    return JsonResponse({'jareaList': jareaList})


def updateDefaultAddr(request):
    addrid = request.GET.get('addrid', -1)
    addrid = int(addrid)

    # 修改数据
    Address.objects.filter(id=addrid).update(isdefault=True)
    Address.objects.exclude(id=addrid).update(isdefault=False)

    return HttpResponseRedirect('/user/address/')