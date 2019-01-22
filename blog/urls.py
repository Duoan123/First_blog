"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog_app import views
from blog_app import urls as blog_app_urls
from blog_app.view_jiyan import jiyan
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    #登陆验证
    url(r'^$',views.home),
    url(r'^index/$', views.home),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^check.png/$', views.check),

    #注册
    url(r'^reg/$', views.reg),
    #上传例子
    url(r'^upload/$', views.upload),

    #将个人主页的博客，分流到blog_app下的urls.py
    url(r"^blog_app/", include(blog_app_urls)),

    #富文本编辑器上传图片
    url(r'^edit_upload/', views.edit_upload),
    

    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register', jiyan.get_geetest),
    url(r'^login2/$',jiyan.login2),

    #配置media路由，让头像显示在浏览器
    url(r'^media/(?P<path>.*)$',serve,{"document_root":settings.MEDIA_ROOT}),

    url(r'^test/$',views.test),
    



    
]
