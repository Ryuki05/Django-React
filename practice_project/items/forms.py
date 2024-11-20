from django import forms
from . models import Items_table

## 登録フォーム
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Items_table
        fields = ['name','price','stock','category']
        labels = {
            'name':"名前",
            'price':"価格",
            'stock':"在庫数",
            'category':"カテゴリ",
        }

## 検索フォーム
class FindForm(forms.Form):
    find = forms.CharField(
        label='検索',
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        )
