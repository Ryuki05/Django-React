from django.db import models
from django.core.validators import ValidationError
from django.core.validators import MinLengthValidator
from django.core.validators import URLValidator
from django.core.validators import RegexValidator
import re

# Create your models here.
# 数字のバリデーター関数
def number_only(value):
    if (re.match(r"^[0-9]*$",value) == None):
        raise ValidationError(
            "%(value)s is not Number!",
            params = {"value": value}
        )

class Friend(models.Model):
    # name = models.CharField(max_length=100,validators=[
    #     MinLengthValidator(10),      # Ensure this value has at least 10 characters (it has 8).
    #     URLValidator(),              # Enter a valid URL.
    #     RegexValidator(r'^[a-z]*$'), # Enter a valid value.
    #     number_only                  # aaaa is not Number!
    #     ])
    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    gender = models.BooleanField()
    age = models.IntegerField(default=0)
    birthday = models.DateField()

    def __str__(self):
        return "<Friend:id=" + str(self.id) + "," + self.name + "(" + str(self.age) + ")>" 


# メッセージモデル
class Message(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<Message:id> = " + str(self.id) + "," + self.title + "(" + str(self.pub_date) + ")>"
    
    class Meta:
        ordering = ("pub_date",)

