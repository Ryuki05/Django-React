from django.shortcuts import render
from django.shortcuts import redirect
from sns.forms import PostForm
from sns.models import Message,Good
from django.core.paginator import Paginator
from sns.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='/admin/login/')
def index(request,page=1):

    form = PostForm(request.user)
    msgs = Message.objects.all()
    paginator = Paginator(msgs,5)
    page_items = paginator.get_page(page)

    params = {
        'login_user':request.user,
        'form':form,
        'contents':page_items,
    }
    return render(request, "sns/index.html",params)

@login_required(login_url='/admin/login/')
def post(request):
    
    if request.method == 'POST':
        # 送信内容を取得
        content = request.POST['content']

        # メッセージを保存
        msg = Message()
        msg.owner = request.user
        msg.content = content
        msg.save()

        # リダイレクト
        return redirect(to = '/sns')

    else:
        msgs = Message.objects.filter(owner = request.user).all()
        params = {
            'login_user':request.user,
            'contents':msgs
        }

        return render(request,"sns/post.html",params)
    
@login_required(login_url='/admin/login/')
def goods(request):
    
    goods = Good.objects.filter(owner=request.user).all()

    params = {
        'login_user':request.user,
        'contents':goods,
    }
    return render(request,'sns/good.html',params)


@login_required(login_url='/admin/login/')
def good(request,good_id):

    # goodされたメッセージの取得
    good_msg = Message.objects.get(id=good_id)

    # goodした回数
    is_good = Good.objects.filter(owner=request.user).filter(message=good_msg).count()

    # good済み処理
    if is_good > 0:
        messages.success(request,"既にメッセージにはGoodしています。")
        return redirect(to='/sns')

    # good未の処理
    # goodの数を増やす
    good_msg.good_count += 1
    good_msg.save()

    # Goodテーブルを作成
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()
    messages.success(request,"メッセージにGoodしました。")
    return redirect(to='/sns')
