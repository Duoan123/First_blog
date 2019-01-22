import os
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
    import django
    django.setup()
    from blog_app import models
    from django.db.models import Count

    user_obj = models.UserInfo.objects.filter(username="gkxadmin")
    blog_obj = models.UserInfo.objects.filter(username="gkxadmin").first().blog
    print(blog_obj)
    category = models.Category.objects.filter(blog=blog_obj).annotate(c=Count("article")).values("title","c")
    print(category)
    ret = models.UserInfo.objects.values("username","phone")
    ret2 = models.UserInfo.objects.values_list("username","phone")
    print(ret)
    print(ret2)
    ret3 = models.Article.objects.filter(user_id=1)
    print("取外键的值",ret3)
    ret4 = models.Tag.objects.filter(blog_id=1)
    print(ret4)
    ret5 = models.Tag.objects.raw("select title from blog_app_tag")
    print(ret5)
    ret6 = article_list = models.Category.objects.filter(nid=1).first().article_set.all()
    print(ret6)

    # ret = models.Article.objects.filter(user=user_obj).extra(
    #     select={"date":"select date_format(create_time,'%%Y-%%m')","ddd":"select count(1) from blog_app_blog"}
    # ).values("title","date","ddd")
    # print(ret)
    #
    # ret2 = models.UserInfo.objects.filter(username="gkxadmin").extra(
    #     select={"ddd":"select count(1) from blog_app_blog"}
    # ).values("ddd")
    # print(ret2)

    # archive_list = models.Article.objects.filter(user=user_obj).extra(
    #     select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
    # ).values("archive_ym").annotate(n=Count("nid")).values("archive_ym","n")
    # archive_list = archive_list.annotate(n=Count("nid")).values("archive_ym","n")
    # print(archive_list)
# <QuerySet [{'archive_ym': '2018-11', 'n': 1}, {'archive_ym': '2017-11', 'n': 1}]>

    # archive_list = models.Article.objects.filter(user=user_obj).extra(
    #     select={"archive_y": "date_format(create_time,'%%Y')", "archive_m": "date_format(create_time,'%%m')"}
    # ).values("archive_y","archive_m",).annotate(n=Count("nid")).values("archive_y", "archive_m", "n")
    # print(archive_list)