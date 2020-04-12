import json, time
from datetime import date, timedelta
from django.db import transaction
from django.http import JsonResponse,HttpResponse
from redis import Redis
from admin.models import User
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt

# Redis 服务端配置
red = Redis(host='127.0.0.1', port=6379)

# 用户信息
def get_user(request):
    rows = request.GET.get('rows')
    page = request.GET.get('page', 1)
    users = User.objects.all().order_by('id')
    all_page = Paginator(users, rows)
    try:
        page_obj = all_page.page(page).object_list
    except EmptyPage:
        page_obj = all_page.page(int(page)-1).object_list
    page_data = {
        'page': page,
        'total': all_page.num_pages,
        'records': all_page.count,
        'rows': list(page_obj)
    }
    # 分页
    def my_default(u):
        if isinstance(u,User):
            return {
                'id': u.id,
                'username': u.username,
                'religious_name': u.religious_name,
                'state': u.state,
                'address': u.address,
                'head_img': str(u.head_img),
                'gender': u.gender,
                'phone': u.phone,
                'mail': u.mail,

            }
    data = json.dumps(page_data, default=my_default)
    return HttpResponse(data)

# 添加用户
@csrf_exempt                # @csrf_exempt 类的视图跨域  csrf防御机制，即跨站请求伪造
def add_user(request):
    try:
        username = request.POST.get("username")
        religious_name = request.POST.get('religious_name')
        state = request.POST.get('state')
        address = request.POST.get('address')
        head_img = request.FILES.get('head_img')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        mail = request.POST.get('mail')
        with transaction.atomic():
            result = User.objects.create(username=username,
                                          religious_name=religious_name,
                                          state=state,
                                          address=address,
                                          head_img=head_img,
                                          gender=gender,
                                          phone=phone,
                                          mail=mail,
                                          )
            if result:
                return HttpResponse(1)
    except:
        return  HttpResponse(0)

# 用户信息修改
@csrf_exempt
def edit(request):

    user_id = request.POST.get('id')
    # user_name= request.POST.get('username')
    user = User.objects.filter(id=user_id)
    def my_default(u):
        if isinstance(u, User):
            return {

                'username': u.username,
                'religious_name': u.religious_name,
                'state': u.state,
                'address': u.address,
                'gender': u.gender,
                'phone': u.phone,
                'mail': u.mail,
            }
    return JsonResponse({'data': list(user)}, json_dumps_params={"default": my_default})

# 信息修改提交
@csrf_exempt
def edit_logic(request):
    try:
        user_id = request.POST.get('id')
        user = User.objects.filter(id=user_id)[0]
        user.username = request.POST.get('username')
        user.religious_name = request.POST.get('religious_name')
        user.state = request.POST.get('state')
        user.address = request.POST.get('address')
        img = request.FILES.get('head_img')
        with transaction.atomic():
            if img == None:
                user.head_img = user.head_img
            else:

                user.head_img = img
            user.gender = request.POST.get('gender')
            user.phone = request.POST.get('phone')
            user.mail = request.POST.get('mail')
            user.save()
            return HttpResponse(1)
    except:
        return HttpResponse(0)


@csrf_exempt
def operate(request):
    try:
        option = request.POST.get('oper')
        if option == 'del':
            user_id = request.POST.get('id')
            with transaction.atomic():
                User.objects.get(pk=user_id).delete()
                return HttpResponse('success')
    except:
        return HttpResponse(0)

# 月份周期
def get_data(request):

    if red.get('data'):
        data = eval(red.get('data'))
    else:
        today = time.strftime('%Y-%m-%d')
        day1 = (date.today() + timedelta(days=-7)).strftime("%Y-%m-%d")
        day2 = (date.today() + timedelta(days=-6)).strftime("%Y-%m-%d")
        day3 = (date.today() + timedelta(days=-5)).strftime("%Y-%m-%d")
        day4 = (date.today() + timedelta(days=-4)).strftime("%Y-%m-%d")
        day5 = (date.today() + timedelta(days=-3)).strftime("%Y-%m-%d")
        day6 = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d")
        day7 = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        days = [today, day7, day6, day5, day4, day3, day2, day1]
        user = []
        for i in range(7):
            count = User.objects.filter(register_data__range=[days[i + 1], days[i]]).count()
            user.append(count)
        data = {'x': days[:7], 'y': user}
        red.set('data', str(data), 24 * 60 * 60)
    return JsonResponse(data)

# 地址
def get_map(request):
    if red.get('user'):
        data = eval(red.get('user'))
        print(1)
    else:
        data = [
            {'name': '北京', 'value': User.objects.filter(address="北京").count()},
            {'name': '天津', 'value': User.objects.filter(address="天津").count()},
            {'name': '上海', 'value': User.objects.filter(address="上海").count()},
            {'name': '重庆', 'value': User.objects.filter(address="重庆").count()},
            {'name': '河北', 'value': User.objects.filter(address="河北").count()},
            {'name': '河南', 'value': User.objects.filter(address="河南").count()},
            {'name': '云南', 'value': User.objects.filter(address="云南").count()},
            {'name': '辽宁', 'value': User.objects.filter(address="辽宁").count()},
            {'name': '湖南', 'value': User.objects.filter(address="湖南").count()},
            {'name': '安徽', 'value': User.objects.filter(address="安徽").count()},
            {'name': '山东', 'value': User.objects.filter(address="山东").count()},
            {'name': '新疆', 'value': User.objects.filter(address="新疆").count()},
            {'name': '江苏', 'value': User.objects.filter(address="江苏").count()},
            {'name': '浙江', 'value': User.objects.filter(address="浙江").count()},
            {'name': '江西', 'value': User.objects.filter(address="江西").count()},
            {'name': '湖北', 'value': User.objects.filter(address="湖北").count()},
            {'name': '广西', 'value': User.objects.filter(address="广西").count()},
            {'name': '甘肃', 'value': User.objects.filter(address="甘肃").count()},
            {'name': '山西', 'value': User.objects.filter(address="山西").count()},
            {'name': '陕西', 'value': User.objects.filter(address="陕西").count()},
            {'name': '吉林', 'value': User.objects.filter(address="吉林").count()},
            {'name': '福建', 'value': User.objects.filter(address="福建").count()},
            {'name': '贵州', 'value': User.objects.filter(address="贵州").count()},
            {'name': '广东', 'value': User.objects.filter(address="广东").count()},
            {'name': '青海', 'value': User.objects.filter(address="青海").count()},
            {'name': '西藏', 'value': User.objects.filter(address="西藏").count()},
            {'name': '四川', 'value': User.objects.filter(address="四川").count()},
            {'name': '宁夏', 'value': User.objects.filter(address="宁夏").count()},
            {'name': '海南', 'value': User.objects.filter(address="海南").count()},
            {'name': '台湾', 'value': User.objects.filter(address="台湾").count()},
            {'name': '香港', 'value': User.objects.filter(address="香港").count()},
            {'name': '澳门', 'value': User.objects.filter(address="澳门").count()},
            {'name': '内蒙古', 'value': User.objects.filter(address="内蒙古").count()},
            {'name': '黑龙江', 'value': User.objects.filter(address="黑龙江").count()},
        ]
        red.set('user', str(data), 24*60*60)
    return JsonResponse(data, safe=False)

