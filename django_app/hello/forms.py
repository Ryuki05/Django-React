from django import forms
from .models import Friend
from .models import Message

# MessageForm
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["title","content","friend"]
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control form-control-sm"}),
            "content":forms.Textarea(attrs={"class":"form-control form-control-sm"}),
            "friend":forms.Select(attrs={"class":"form-control form-control-sm"}),
        }
        labels = {
            "title":"タイトル",
            "content":"メッセージ",
            "friend":"投稿者",
        }

# checkフォーム
class CheckForm(forms.Form):
    str = forms.CharField(label="文字列",required=True)
    def clean(self):
        cleaned_data = super().clean()
        str = cleaned_data["str"]
        if (str.lower().startswith("no")):
            raise forms.ValidationError("「no」で始まる入力がありました。")

    min = forms.CharField(label="最小入力数",min_length=3) # 最小文字数:3
    max = forms.CharField(label="最大入力数",max_length=5) # 最大文字数:5
    num = forms.IntegerField(label="数値",min_value=10,max_value=50) # 最小値:10,最大値:50
    date = forms.DateField(label="日付",input_formats=["%d"]) # 1～31までの日
    time = forms.TimeField(label="時間") # 時間 17:00
    datatime = forms.DateTimeField(label="日時",input_formats=["Y/m/d H:i"])

# Findフォーム
class FindForm(forms.Form):
    find = forms.CharField(label='Find',required=False,widget=forms.TextInput(attrs={'style':'width:400px;'}))

# モデルフォーム
class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name','mail','gender','age','birthday']
        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "mail":forms.EmailInput(attrs={"class":"form-control"}),
            "age":forms.NumberInput(attrs={"class":"form-control"}),
            "birthday":forms.DateInput(attrs={"class":"form-control"}),
        }


# 登録フォーム
class RegisterForm(forms.Form):
    name = forms.CharField(label='名前',widget=forms.TextInput(attrs={'class':'form-control'}))
    mail = forms.EmailField(label='メールアドレス',widget=forms.EmailInput(attrs={'class':'form-control'}))
    gender = forms.BooleanField(label='性別',required=False,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    age = forms.IntegerField(label='年齢',widget=forms.NumberInput(attrs={'class':'form-control'}))
    birthday = forms.DateField(label='生年月日',widget=forms.DateInput(attrs={'class':'form-control'}))

# SearchForm ID検索フォーム
class SearchForm(forms.Form):
    id = forms.IntegerField(label='ID検索',widget=forms.TextInput(attrs={'class':'form-control'}))

# HelloForm
class HelloForm(forms.Form):
    name = forms.CharField(label="名前",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    mail = forms.URLField(label="メールアドレス",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.IntegerField(label="年齢",required=True,widget=forms.NumberInput(attrs={'class':'form-control'}))

# サンプルフォーム
class SampleForm(forms.Form):
    # input type="text"
    text = forms.CharField(label="テキスト")

    # input type="email"
    mail = forms.EmailField(label="メールアドレス")

    # input type="number"
    number = forms.IntegerField(label="ナンバー")

    # input type="number" step="0.1"
    number_float = forms.FloatField(label="浮動小数")

    # input type="url"
    url = forms.URLField(label="URL")

    # input type="date" 例) 2024-06-19 2024/06/19
    date = forms.DateField(label="日付")

    # input type="time"  例) 15:30:40
    time = forms.TimeField(label="時刻")

    # input type="datetime-local" 例) 2024-06-19 15:30:40
    dateTime = forms.DateTimeField(label="日時")

    # input type="checkbox"
    check = forms.BooleanField(label="チェックボックス",required=False)

    # select
    data = [("A","item1"),("B","item2"),("C","item3")]
    select = forms.ChoiceField(label="セレクト",choices=data,widget=forms.Select())

    # input type="radio"
    radio = forms.ChoiceField(label="ラジオ",choices=data,widget=forms.RadioSelect())

    # input type="chechbox" 複数選択
    checkbox = forms.MultipleChoiceField(label="複数選択",choices=data,widget=forms.SelectMultiple())


class SessionForm(forms.Form):
    session = forms.CharField(label="セッション")

