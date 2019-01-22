import os

'''

Admin的实现流程：
1 启动：
      import admin
      def autodiscover():
           autodiscover_modules('admin', register_to=site)
       执行每一个app下的admin.py文件
       
2 注册
      单例模式
    
3 设计URL

'''

'''
1.在app下的admin中 注册models中的每一个类
admin.site.register(models.UserInfo)

2.访问url 127.0.0.1:8000/admin/
    进入admin后台管理

3.添加数据

4.其余设置：
    settings中可以设置admin的语言显示  LANGUAGE_CODE = 'zh-hans'  # 默认是 LANGUAGE_CODE = 'en-us'
    verbose_name ： 可以给字段设置，也可以在元信息中给整个类设置别名
    
===========================================admin常用参数配置===========================================
全部参数可以看博客：

from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
# Register your models here.
class BookConfig(admin.ModelAdmin):
    def deletes(self):                      #新增一个方法，显示一个a标签的删除按钮，需要配合list_display使用
        return mark_safe("<a href='#'>删除</a>")

    list_display = ["title","price","publishDate",deletes] #在book的url里设置显示字段，可以把上面设置的方法放进来
                                                              #切记！ 多对多字段不能添加
    list_display_links = ["price"] #把列表里的字段设置为连接，点击可以进入change页面
    list_filter = ["price","title","publish"] #将列表中的字段作为分类，显示在右侧。bug：当一对多字段只有一个值的时候，不会显示
    list_editable = ["title"]     #将列表中的字段在主页中变为可编辑状态
    fields = ('title',)           #自定义编辑页面显示的字段，此时编辑book表，只显示title这个字段
                                  #因此只能隐藏那些可为空的字段，减少用户输入
    #change_list_template = "list_html"  # 源码中 django-contrib-admin-templates-admin 配置了admin页面所有的html文件
                                         # 此时表示用我们新写的 list_html页面 替换源码中的 change_list文件

    def patch_init(self,request,queryset):
        queryset.update(price=100)   # 执行 price=100 的更新操作
    patch_init.short_description = "批量初始化" #设置快捷描述
    actions = ['patch_init',]       #将我们定义的更新操作，注册进action

admin.site.register(Book,BookConfig)
'''