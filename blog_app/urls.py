from django.conf.urls import url
from blog_app import views

urlpatterns = [
    # 访问个人主页文章
    url(r'(\w+)/article/(\d+)/$', views.article_detail),  # 文章详情  article_detail(request, xiaohei, 1)
    # url(r'^article/(\d+)/$', views.article_detail),

    #访问文章分类
    url(r'^(?P<username>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*)/$', views.filter_show),

    #点赞
    url(r"^updown_acount/$", views.updown_acount),

    #提交评论
    url(r"^comment_up/$", views.comment_up),

    #获取评论树需要用到的数据
    url(r"^comment_tree/(\d+)/$",views.comment_tree),

    #后台添加文章
    url(r"^backend/add_article/$",views.add_article),

    #访问个人博客主页
    url(r"^(\w+)/$", views.blog),

]