from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#九张表：用户表 博客表 博客分类表 标签表 文章表 文章详情表 文章标签关系表 点赞表 评论表
class UserInfo(AbstractUser):
    """
    用户信息表
    """
    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11,null=True,unique=True)
    avatar = models.FileField(upload_to="avatars/",default="avatars/default.png",verbose_name="头像") #verbose_name 在admin中让该字段显示为 “头像”
    create_time = models.DateTimeField(auto_now_add=True)
    blog = models.OneToOneField(to="Blog",to_field="nid",null=True)

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name #默认会当做是复数，然后变成 用户s ，这里让两者相等，当复数时不加s

class Blog(models.Model):
    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64) #博客标题
    site = models.CharField(max_length=32,unique=True) #博客后缀
    theme = models.CharField(max_length=32) #博客主题

    def __str__(self):
        return self.title

class Category(models.Model):
    """
    个人博客文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32) #标题分类
    blog = models.ForeignKey(to="Blog",to_field="nid")  #外键关联博客，一个分类可以有很多篇博客，一个博客也可以有很多个分类

    def __str__(self):
        return self.title

class Tag(models.Model):
    """
    标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)  #标签名
    blog = models.ForeignKey(to="Blog",to_field="nid")  #所属博客

    def __str__(self):
        return self.title

class Article(models.Model):
    """
    文章
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50) #文章标题
    desc = models.CharField(max_length=255) #文章描述
    # create_time = models.DateTimeField(auto_now_add=True)   #创建时间
    create_time = models.DateTimeField(auto_now_add=True)   #创建时间

    category = models.ForeignKey(to="Category",to_field="nid",null=True)
    user = models.ForeignKey(to="UserInfo",to_field="nid")
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=("article","tag"), #这种方式建关联表称为中介模型
    )                                       #此处第一个字段一定要填，设置多对多字段的表，也就是多对多设置在哪里第一个字段就填这张表

    #评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    # 踩
    down_count = models.IntegerField(verbose_name="踩数", default=0)

    def __str__(self):
        return self.title

class ArticleDetail(models.Model):
    """
    文章详情表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article",to_field="nid")

    def __str__(self):
        return "{}---->全文".format(self.article.title)

class Article2Tag(models.Model):
    """
    文章和标签的多对多关系表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article",to_field="nid")
    tag = models.ForeignKey(to="Tag",to_field="nid")

    def __str__(self):
        return "%s----->%s标签"%(self.article.title,self.tag.title)

    class Meta:
        unique_together = (("article","tag"),)

class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo",null=True)
    article = models.ForeignKey(to="Article",null=True)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article","user"),)

class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article",to_field="nid")
    user = models.ForeignKey(to="UserInfo",to_field="nid")
    content = models.CharField(max_length=255)              #评论内容
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self",null=True,blank=True)

    def __str__(self):
        return self.content

