from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import HelloForm
from .forms import SampleForm
from .forms import SessionForm
from .forms import SearchForm
from .forms import RegisterForm
from .forms import FriendForm
from .forms import MessageForm
from .forms import FindForm
from .forms import CheckForm

from django.views.generic import TemplateView
from .models import Friend
from .models import Message
from django.db.models import Q
from django.db.models import Count,Sum,Avg,Min,Max

# ページネーション
from django.core.paginator import Paginator

# メッセージ関数
def message(request, page=1):
    if (request.method=="POST"):
        obj = Message()
        form = MessageForm(request.POST,instance=obj)
        form.save()

    data = Message.objects.all().reverse()
    paginator = Paginator(data,5)
    params = {
        "title":"Message",
        "form":MessageForm(),
        "data":paginator.get_page(page),
    }

    return render(request, "hello/message.html",params)


def check(request):
    params = {
        "title":"Hello Check",
        "message":"チェック バリデーション",
        "form":FriendForm()
    }

    if (request.method == "POST"):

        obj = Friend()
        form = FriendForm(request.POST,instance=obj)
        params["form"] = form

        if (form.is_valid()):
            params["msg"] = "OK!"
        else:
            params["msg"] = "no good!"

    return render(request,"hello/check.html",params)


## check
# def check(request):
#     params = {
#         "title":"Hello Check",
#         "message":"チェック バリデーション",
#         "form":CheckForm()
#     }

#     if (request.method == "POST"):
#         form = CheckForm(request.POST)
#         params["form"] = form

#         if (form.is_valid()):
#             params["msg"] = "OK!"
#         else:
#             params["msg"] = "no good!"

#     return render(request,"hello/check.html",params)


## find
def find(request):

    if (request.method == 'POST'):
        form = FindForm(request.POST)
        find = request.POST['find'] # リクエストパラメータの取得
        # value = find.split() # ["10","20"]

        ### 文字列検索
        # data = Friend.objects.filter(name=find) # 名前検索
        # data = Friend.objects.filter(name__contains=find) # あいまい検索
        # data = Friend.objects.filter(name__icontains=find) # 大文字小文字区別なし
        # data = Friend.objects.filter(name__istartswith=find) # 先頭検索
        # data = Friend.objects.filter(name__iendswith=find) # 末尾検索
        # data = Friend.objects.filter(name__iexact=find) # 完全一致検索 大文字小文字区別なし
        ### 数値検索
        # data = Friend.objects.filter(age=int(find)) # 年齢検索
        # data = Friend.objects.filter(age__gt=int(find)) # より大きい
        # data = Friend.objects.filter(age__gte=int(find)) # 以上
        # data = Friend.objects.filter(age__lt=int(find)) # より小さい
        # data = Friend.objects.filter(age__lte=int(find)) # 以下
        ### 複数条件
        # data = Friend.objects.filter(age__gte=int(value[0]),age__lte=int(value[1])) # ~以上~以下 
        # data = Friend.objects.filter(Q(name__contains=find) | Q(mail__contains=find)) # 2件以上の検索
        # data = Friend.objects.all()[int(value[0]):int(value[1])]
        # msg = 'Result:' + str(data.count())

        # data = Friend.objects.all()

        sql = "select * from hello_friend"

        if (find != ""):
            sql += " where " + find

        data = Friend.objects.raw(sql)

        re1 = Friend.objects.aggregate(Count("age"))
        re2 = Friend.objects.aggregate(Sum("age"))
        re3 = Friend.objects.aggregate(Avg("age"))
        re4 = Friend.objects.aggregate(Min("age"))
        re5 = Friend.objects.aggregate(Max("age"))

        print(re1,re2,re3,re4,re5) 
        ### {'age__count': 5} {'age__sum': 111} {'age__avg': 22.2} {'age__min': 7} {'age__max': 39}


        msg = "Count:" + str(re1["age__count"]) + "<br>"\
            + "Sum:" + str(re2["age__sum"]) + "<br>"\
            + "Avg:" + str(re3["age__avg"]) + "<br>"\
            + "Min:" + str(re4["age__min"]) + "<br>"\
            + "Max:" + str(re5["age__max"])
 
    else:
        msg = "検索ワード"
        form = FindForm()
        data = Friend.objects.all().order_by("age").reverse()

    params = {
        'title' : "Hello",
        'message' : msg,
        'form' : form,
        'data' : data,
    }

    return render(request, 'hello/find.html', params)

## detail
def detail(request,num):
    obj = Friend.objects.get(id=num) # id指定でデータを取得
    params = {
        'title':"Hello",
        'message':"詳細",
        'id':num,
        'obj':obj
    }
    return render(request,'hello/detail.html',params)

## delete
def delete(request,num):
    obj = Friend.objects.get(id=num) # id指定でデータを取得

    if(request.method=='POST'):
        obj.delete()

        return redirect(to='/hello') # リダイレクト

    params = {
        'title':"Hello",
        'message':"削除",
        'id':num,
        'obj':obj
    }
    return render(request,'hello/delete.html',params)

## edit
def edit(request,num):
    obj = Friend.objects.get(id=num) # id指定でデータを取得

    # postリクエストされた場合
    if(request.method=='POST'):

        # 登録処理と同じ
        friend = FriendForm(request.POST,instance=obj)
        friend.save()

        return redirect(to='/hello') # リダイレクト

    params = {
        'title':"Hello",
        'message':"更新",
        'id':num,
        'form':FriendForm(instance=obj), # 取得したオブジェクトをフォームに入れる
    }
    return render(request,'hello/edit.html',params)

## create
def create(request):
    params = {
        'title':"Hello",
        'message':"登録",
        'form':FriendForm(),
    }

    if(request.method=='POST'):
        obj = Friend()
        # name = request.POST['name']
        # mail = request.POST['mail']
        # gender = 'gender' in request.POST
        # age = int(request.POST['age'])
        # birthday = request.POST['birthday']
        # firend = Friend(name=name,mail=mail,gender=gender,age=age,birthday=birthday)
        friend = FriendForm(request.POST,instance=obj)
        friend.save()

        # 保存が出来たらindexへリダイレクト
        return redirect(to='/hello')

    return render(request,'hello/create.html', params)

## index
def index(request,num=1):

    data = Friend.objects.all()
    page = Paginator(data,3)

    params = {
        'title':"Hello",
        'message':"Friend一覧",
        'form':SearchForm(),
        'data':page.get_page(num)
    }

    if (request.method=='POST'):
        params['form'] = SearchForm(request.POST) # 検索フォーム

        num = request.POST['id']    # リクエストパラメータの取得
        try:
            item = Friend.objects.get(id=num)  # クエリセットの取得
            params['data'] = [item]
        except:
            params['msg'] = "データが見つかりませんでした。"
            params['data'] = Friend.objects.all().values('id','name')
    
    return render(request,'hello/index.html',params)



# def index(request):

#     params = {
#         'title':"Hello",
#         'message':"Friend一覧",
#         'form':SearchForm(),
#         'data':[]
#     }

#     if (request.method=='POST'):
#         params['form'] = SearchForm(request.POST) # 検索フォーム

#         num = request.POST['id']    # リクエストパラメータの取得
#         try:
#             item = Friend.objects.get(id=num)  # クエリセットの取得
#             params['data'] = [item]
#         except:
#             params['msg'] = "データが見つかりませんでした。"
#             params['data'] = Friend.objects.all().values('id','name')
            
#     else:
#         params['data'] = Friend.objects.all().values()
       
#     return render(request,'hello/index.html',params)


## セッション
def sessionSample(request):
    params = {
        'msg':"",
        'form':SessionForm(),
    }

    if request.method=="GET":
        msg = request.session.get("Last_msg","No message")
        params['msg'] = msg

    if request.method=="POST":
        ses = request.POST['session']
        
        request.session['Last_msg'] = ses
        params['msg'] = "send:" + ses

    return render(request,'hello/sessionSample.html',params)

def sample(request):
    params = {
        'msg':"",
        'form':SampleForm(),
    }

    if(request.method=='POST'):
        text = request.POST['text']
        mail = request.POST['mail']
        number = request.POST['number']
        number_float = request.POST['number_float']
        url = request.POST['url']
        date = request.POST['date']
        time = request.POST['time']
        dateTime = request.POST['dateTime']

        # チェックボックス
        if ('check' in request.POST):
            check = "Checked"
        else:
            check = "none Checked"

        select = request.POST['select']
        radio = request.POST['radio']

        # 複数選択はリストで取得
        check_list = request.POST.getlist('checkbox')


        msg= (text,mail,number,number_float,url,date,time,dateTime,check,select,radio,check_list)
        params['msg'] = msg
    return render(request,'hello/formSample.html',params)

class HelloView(TemplateView):

    # 初期化
    def __init__(self):
        self.params = {
            'title':"Hello/Index2",
            'message':"あなたのデータ:",
            'form':HelloForm(),
        }

    # GET送信されて来た場合のメソッド
    def get(self,request):
        return render(request,"hello/index2.html",self.params)

    # POST送信されて来た場合のメソッド
    def post(self,request):
        name = request.POST['name']
        mail = request.POST['mail']
        age = request.POST['age']

        msg = "あなたは、"+ name + "(" + age + ")です。<br>メールアドレスは" + mail + "ですね。" 

        self.params['message'] = msg
        self.params['form'] = HelloForm()

        return render(request,'hello/index2.html',self.params)

# indexのページ
# def index(request):

#     params = {
#         'title':"Hello/index",
#         'msg':"あなたのデータを入力",
#         'form': HelloForm()
#     }

#     # リクエストパラメータがあった場合
#     if (request.method == 'POST'):

#         # リクエストパラメータの取得
#         name = request.POST['name']
#         mail = request.POST['mail']
#         age = request.POST['age']
        
#         params['msg'] = "名前:" + name + "<br>メールアドレス:" + mail + "<br>年齢:" + age

#         params['form'] = HelloForm(request.POST)

#     return render(request,'hello/index.html',params)

def form(request):
    # リクエストパラメータの取得
    msg = request.POST['msg']
    params = {
        'title':"Hello/form",
        'msg':"こんにちは" + msg + "さん"
    }

    return render(request,'hello/index.html',params)

# nextのページ
def next(request):

    params = {
        'title':"Hello/next",
        'msg':"もう一つのページ",
        # 'goto':'index',
    }

    return render(request,'hello/index.html',params)










