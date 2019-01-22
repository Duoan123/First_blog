from django import forms
from django.forms import widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from blog_app import models
class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="用户名",
        error_messages={
            "required":"用户名不能为空",
        },
        # widget控制的是生成html代码相关的
        widget = widgets.TextInput(attrs={"class":"form-control"})
    )
    password = forms.CharField(
        min_length=6,
        label="密码",
        error_messages={
            "required":"密码不能为空",
            "max_length":"密码至少要6位"
        },
        widget = widgets.PasswordInput(attrs={"class":"form-control"},render_value=True) #可以设置render_value=True
    )
    re_pwd = forms.CharField(
        min_length=6,
        label="确认密码",
        error_messages={
            "required":"确认密码不能为空",
            "max_length": "确认密码至少要6位"
        },
        widget = widgets.PasswordInput(attrs={"class":"form-control"},render_value=True) #可以设置render_value=True
    )
    email = forms.EmailField(
        label="邮箱",
        error_messages={
          "required":"邮箱不能为空",
            "invalid":"邮箱格式不正确",
        },
        widget=widgets.EmailInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="手机",
        max_length=11,
        validators=[
            RegexValidator(r'[0-9]+$','手机号必须是数字'),
            RegexValidator(r'^1[3-9][0-9]{9}$','手机格式有误')
        ],
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        error_messages={"required":"手机号不能为空"},
    )
    #局部钩子
    def clean_username(self):
        value = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=value)
        if "wwl" in value:
            self.add_error("username", ValidationError("不能包含wwl"))
            # raise ValidationError("不能包含wwl")
        if is_exist:
            self.add_error("username",ValidationError("用户名已存在"))
        return value

    #全局钩子
    def clean(self):
        password = self.cleaned_data.get("password")
        re_pwd = self.cleaned_data.get("re_pwd")
        if re_pwd and re_pwd != password:
            self.add_error("re_pwd",ValidationError("两次密码不一致"))
            # raise ValidationError("两次密码不一致")
        return self.cleaned_data




















