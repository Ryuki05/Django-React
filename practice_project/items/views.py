from django.shortcuts import render
from django.shortcuts import redirect
from . models import Items_table
from . forms import RegisterForm 
from . forms import FindForm
from django.db.models import Q


# Create your views here.

## index
def index(request):

    params = {
        'title': "商品管理",
        'subtitle':"INDEX",
    }

    return render(request, 'items/index.html', params)

## register
def register(request):

    if (request.method == 'POST'):
        obj = Items_table()
        items = RegisterForm(request.POST,instance=obj)
        items.save()

        return redirect(to="/items/items_list")

    params = {
        'title': "商品管理",
        'subtitle':"商品登録",
        'form':RegisterForm(),
    }

    return render(request, 'items/register.html', params)


## list
def items_list(request):

    if (request.method=='POST'):
        find = request.POST['find']

        if len(find)==0:
            obj = Items_table.objects.all()
            form = FindForm(request.POST)
        else:
            value = find.split()
            obj = Items_table.objects.filter(Q(name__in=value) | Q(category__in=value))
            form = FindForm(request.POST)
    else:
        obj = Items_table.objects.all()
        form = FindForm()

    params = {
        'title': "商品管理",
        'subtitle':"商品一覧",
        'form': form, 
        'obj':obj,
    }

    return render(request, 'items/items_list.html', params)


## detail
def detail(request,num):
    obj = Items_table.objects.get(id=num)
    params = {
        'title': "商品管理",
        'subtitle':"商品詳細",
        'item':obj,
    }

    return render(request, 'items/detail.html', params)


## delete
def delete(request,num):
    obj = Items_table.objects.get(id=num)

    if(request.method=='POST'):
        ans = request.POST['ans']
        if ans=="yes":
            obj.delete()
            return redirect(to='/items/items_list')

    params = {
        'title': "商品管理",
        'subtitle':"商品削除",
        'item':obj,
    }

    return render(request, 'items/delete.html', params)

## edit
def edit(request,num):
    obj = Items_table.objects.get(id=num)

    if(request.method=='POST'):
        item = RegisterForm(request.POST,instance=obj)
        item.save()
        return redirect(to='/items/items_list')

    params = {
        'title': "商品管理",
        'subtitle':"商品更新",
        'item':obj,
        'form':RegisterForm(instance=obj),
    }

    return render(request, 'items/edit.html', params)
