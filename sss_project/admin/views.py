from redis import Redis
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from send import API_KEY                #封装API_KEY，调用send模块里的API_KEY
from tools.send_mess import YunPian
from tools.random_code import send_code
from admin.models import Admin

# Redis 服务端配置
red = Redis(host='127.0.0.1', port=6379)

# 首页
def home(request):
    return render(request, 'home.html')

# 登录
def login(request):
    return render(request, 'login.html')

# 短信验证码
@csrf_exempt
def get_code(request):
    mobile = request.POST.get('mobile')
    code = red.get(mobile+"_1")
    if code:
        return HttpResponse(0)
    else:
        if Admin.objects.filter(password=mobile):
            yun_pian = YunPian(API_KEY)
            code = send_code()
            yun_pian.send_message(mobile, code)
            print(mobile, code)
            code1 = red.set(mobile+'_1', code, 120)
            code2 = red.set(mobile+'_2', code, 600)
            return HttpResponse(1)
        else:
            return HttpResponse(3)

# 短信验证码验证
@csrf_exempt
def check_user(request):
    try:
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')
        print(mobile, code)
        code2 = red.get(mobile+'_2').decode()
        print(code2)
        if mobile != '' and code != '' and code == code2:
            # request.session['username'] = mobile
            # request.session['userpwd'] = mobile
            return HttpResponse(1)
        else:
            return HttpResponse(0)
    except AttributeError:
        return HttpResponse(3)