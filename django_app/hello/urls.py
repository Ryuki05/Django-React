from django.urls import path
from . import views
from hello.views import HelloView

urlpatterns = [
    path('',views.index,name='index'),
    path('<int:num>',views.index,name='index'),
    path('next',views.next,name='next'),
    path('form',views.form,name='form'),
    path('index2',HelloView.as_view(),name='index2'),
    path('formSample',views.sample,name='formSample'),
    path('sessionSample',views.sessionSample,name='sessionSample'),
    path('create',views.create,name='create'),
    path('edit/<int:num>',views.edit,name='edit'),
    path('delete/<int:num>',views.delete,name='delete'),
    path('detail/<int:num>',views.detail,name='detail'),
    path('find',views.find, name='find'),
    path('check',views.check, name='check'),
]
