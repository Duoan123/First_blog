from django import template
from django.db.models import Count
from blog_app import models
register = template.Library()

@register.inclusion_tag("left_tag.html")
def left_tag(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    article_list = models.Article.objects.filter(user=user_obj)
    blog_obj = user_obj.blog

    #文章分类
    # category_list = models.Category.objects.filter(blog=blog_obj).annotate(c=Count("article")).values("title","c") #先把指定博客的所有分类取出，然后对这些分类进行分组，并添加一个名为c的字段用来对分类中的文章进行计数，然后再select出分类名和这个count值
    category_list = models.Category.objects.filter(blog=blog_obj)
    #标签分类
    tag_list = models.Tag.objects.filter(blog=blog_obj)
    #文章按创建年月归档archive
    archive_list = models.Article.objects.filter(user=user_obj).extra(
        select={"archive_y":"date_format(create_time,'%%Y')","archive_m":"date_format(create_time,'%%m')"}
    ).values("archive_y","archive_m").annotate(n=Count("nid")).values("archive_y","archive_m","n")
    return {
        "category_list":category_list,
        "tag_list":tag_list,
        "archive_list":archive_list,
        "username":username,
    }
    #sql语句
    # select date_format(create_time,'%Y') from article where user=user_obj


