from django.shortcuts import render
from api.models import Message2,Good2 # 2に書き換え
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize # 追加
from django.http import HttpResponse # 追加
from django.http import JsonResponse # 追加
from django.contrib.auth.models import User # 追加

import json # 追加

# Create your views here.
page_max = 10 # １ページ当りの表示数

# indexのビュー関数
@login_required(login_url='/admin/login/')
def index(request):

    return render(request, "index.html")

# メッセージの関数:メッセージをjson形式で送る
@login_required(login_url='/admin/login/')
def msgs(request,page=1):
    msgs = Message2.objects.all()

    paginator = Paginator(msgs,page_max)
    page_items = paginator.get_page(page)
    serialized_data = serialize("json",page_items)
    return HttpResponse(serialized_data, content_type="application/json")

# メッセージのページ数を返す
@login_required(login_url='/admin/login/')
def plast(request):
    msgs = Message2.objects.all()

    paginator = Paginator(msgs,page_max)
    last_page = paginator.num_pages
    return JsonResponse({'result':"OK",'value':last_page})


# ユーザー名を返す
@login_required(login_url='/admin/login/')
def usr(request,usr_id):
    if usr_id == -1:
        usr = request.user
    else:
        usr = User.objects.filter(id=usr_id).first()

    return JsonResponse({'result':"OK",'value':usr.username})


# メッセージの送信処理
@login_required(login_url='/admin/login/')
def post(request):
    
    if request.method == 'POST':
        # 送信内容を取得
        byte_data = request.body.decode('utf-8')
        json_body = json.loads(byte_data)
        content = json_body['content']

        # メッセージを設定して保存
        msg = Message2()
        msg.owner = request.user
        msg.owner_name = request.user.username
        msg.content = content
        msg.save()

        return HttpResponse("OK")
    else:
        return HttpResponse("NG")

    
# @login_required(login_url='/admin/login/')
# def goods(request):
    
#     goods = Good2.objects.filter(owner=request.user).all()

#     params = {
#         'login_user':request.user,
#         'contents':goods,
#     }
#     return render(request,'sns/good.html',params)


@login_required(login_url='/admin/login/')
def good(request,good_id):

    # goodされたメッセージの取得
    good_msg = Message2.objects.get(id=good_id)

    # goodした回数
    is_good = Good2.objects.filter(owner=request.user).filter(message=good_msg).count()

    # good済み処理
    if is_good > 0:
        return HttpResponse("NG")

    # good未の処理
    # goodの数を増やす
    good_msg.good_count += 1
    good_msg.save()

    # Good2テーブルを作成
    good = Good2()
    good.owner = request.user
    good.message = good_msg
    good.save()
    return HttpResponse("OK")
