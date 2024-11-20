from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('items_list',views.items_list,name='items_list'),
    path('detail/<int:num>',views.detail,name='detail'),
    path('delete/<int:num>',views.delete,name='delete'),
    path('edit/<int:num>',views.edit,name='edit'),
]