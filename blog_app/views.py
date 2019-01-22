import random
import json
from io import BytesIO
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count,F
from blog_app import models,myforms
from utils.check_code import create_validate_code
from utils.mypage import Page


# Create your views here.

#主页index
# @login_required
def home(request):
    article_list = models.Article.objects.all()
    base_url = request.path_info
    total_count = article_list.count()
    page_obj = Page(request.GET.get("page"), total_count, url_prefix=base_url,per_page=3)
    article_list = article_list[page_obj.start:page_obj.end]
    page_html = page_obj.page_html()
    return render(request,"index.html",{"article_list":article_list,"page_html":page_html})            #用于显示页码

#用户注销
def logout(request):
    '''注销'''
    auth.logout(request)
    return redirect("/index/")

#登陆验证
def login(request):
    '''验证登陆'''
    # if request.is_ajax(): #如果是AJAX请求
    if request.method == "POST":
        data = {"status":0,"msg":""}
        username = request.POST.get("username")
        password = request.POST.get("password")
        valid_code = request.POST.get("valid_code")
        check_code = request.session['check_code']
        next_url = request.POST.get("next")
        print("000000000000",next_url)
        print("网页填写的，后端获取的",valid_code,check_code)
        if check_code and check_code.upper() == valid_code.upper():
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                if next_url and next_url !="false":
                    data["msg"] = next_url
                else:
                    data["msg"] = "/index/"
            else:
                data["status"] = "1"
                data["msg"] = "登陆失败，用户名或者密码有误"
        else:
            data["status"] = "2"
            data["msg"] = "登陆失败，验证码错误"
        return JsonResponse(data)
    return render(request,"login.html")

#生成图片验证码，利用自定义模块 create_validate_code
def check(request):
    f = BytesIO()  #相当于内存里的内存，再通过save把文件写到内存里
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img,code = create_validate_code(size=(120,35),font_size=18,length=4,bg_color=bg_color)
    request.session['check_code'] = code
    print("===============",code)
    img.save(f,'PNG')
    return HttpResponse(f.getvalue())


#ajax提交注册请求
def reg(request):
    form_obj = myforms.RegForm()
    if request.method == "POST":
        ret = {"status":0,"msg":""}
        form_obj = myforms.RegForm(request.POST)
        avatar_img = request.FILES.get("avatar") #获取到ajax提交过来的文件
        if form_obj.is_valid():
            ret["msg"]="/index/"
            # del form_obj.cleaned_data["re_pwd"]
            form_obj.cleaned_data.pop("re_pwd")
            #models中的 FlieField字段，给他传值相当于给他传一个文件，它会自动保存在设置的默认路径，如果出现同名会自动给照片名添加字符，然后再保存到对应路径
            models.UserInfo.objects.create_user(**form_obj.cleaned_data,avatar=avatar_img)

        else:
            ret["status"]="1"
            ret["msg"]=form_obj.errors  #把错误信息传给前端
        return JsonResponse(ret)
    return render(request,"register.html",{"form_obj":form_obj})

#个人主页，blog   person_blog.html
def blog(request,username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    article_list = models.Article.objects.filter(user=user_obj)
    if not user_obj:
        return HttpResponse("访问的博客不存在")
    if user_obj:
        blog_obj = user_obj.blog
        #以下内容被用 母版及inclusion_tag优化了
        # category_obj = models.Category.objects.filter(blog=blog_obj)
        #文章分类
        # category_list = models.Category.objects.filter(blog=blog_obj).annotate(c=Count("article")).values("title","c") #先把指定博客的所有分类取出，然后对这些分类进行分组，并添加一个名为c的字段用来对分类中的文章进行计数，然后再select出分类名和这个count值
        #标签分类
        # tag_list = models.Tag.objects.filter(blog=blog_obj).annotate(c=Count("article")).values("title","c") #同上
        #文章按创建年月归档archive
        # archive_list = models.Article.objects.filter(user=user_obj).extra(
        #     select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
        # ).values("archive_ym").annotate(n=Count("nid")).values("archive_ym", "n")  #年月一起写
        # archive_list = models.Article.objects.filter(user=user_obj).extra(
        #     select={"archive_y":"date_format(create_time,'%%Y')","archive_m":"date_format(create_time,'%%m')"}
        # ).values("archive_y","archive_m").annotate(n=Count("nid")).values("archive_y","archive_m","n")
        return render(request,"person_blog.html",{
            "blog_obj":blog_obj,            #用于页面中导航栏显示博客详情
            "article_list":article_list,    # 文章详情
            "username":username,            #用于 inclusion_tag优化左侧菜单时，传入的参数 {% %}
            # "category_obj":category_list,
            # "tag_list":tag_list,
            # "archive_list":archive_list,
        })

#个人主页中访问文章  person_article.html
def article_detail(request,username,article_id):
    article_obj = models.Article.objects.filter(pk=article_id).first()
    username = article_obj.user.username
    blog_obj = article_obj.user.blog
    comment_list = models.Comment.objects.filter(article_id=article_id)
    return render(request,"person_article.html",{
        "article_obj":article_obj,
        "username":username,
        "blog_obj":blog_obj,
        "comment_list":comment_list,
    })

#查询各个分类下所有的文章 filter_show.html
def filter_show(request,username,condition,val):
    article_list=[]
    user_obj =models.UserInfo.objects.filter(username=username).first()
    blog_obj = user_obj.blog
    if condition == "category":
        article_list = models.Category.objects.filter(nid=val).first().article_set.all()
    if condition == "tag":
        article_list = models.Tag.objects.filter(nid=val).first().article_set.all()
    if condition == "date":
        print(models.Article.objects.filter(user=user_obj))
        article_list = models.Article.objects.filter(user=user_obj).extra(
            where=['date_format(create_time,"%%Y-%%m")=%s'], params=[val, ]).all()
    return render(request,"filter_show.html",{
        "article_list":article_list,
        "username":username,
        "blog_obj":blog_obj,
    })

#点赞实例 person_article.html
def updown_acount(request):
    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))
    user = request.user
    response_data = {"status":True}
    if request.user.username:
        try:
            # 由于user和article设置了联合唯一，因此要进行异常处理，如果不能添加数据，证明出现了异常数据库中已经有这行数据了，也就说明了此时这篇文章这个人已经点赞过了
            models.ArticleUpDown.objects.create(article_id=article_id, user=user,is_up=is_up)
            if is_up:
                models.Article.objects.filter(nid=article_id).update(up_count=F("up_count")+1)
            else:models.Article.objects.filter(nid=article_id).update(down_count=F("down_count")+1)
        except Exception as e:
            ret = models.ArticleUpDown.objects.filter(article_id=article_id,user=user).first().is_up #判断数据库is_up的值，来获取是点赞还是反对
            response_data["status"] = False
            if ret:
                response_data["msg"]="你已经推荐过了"
            else:
                response_data["msg"] = "你已经反对过了"
    else:
        response_data["status"] = False
        response_data["url"] = "1"
        response_data["msg"] = "需要登录："
    return JsonResponse(response_data)
    #还未完成的功能：再点一下可以取消赞，或者取消反对

#提交评论 person_article.html
def comment_up(request):
    print(request.POST)
    response_data = {"status":True}
    comment_content = request.POST.get("comment_content")
    pid = request.POST.get("pid")
    article_id = request.POST.get("article_id")
    if not pid:                         #根评论
        comment_obj =models.Comment.objects.create(article_id=article_id,user=request.user,content=comment_content)
    else:
        comment_obj = models.Comment.objects.create(article_id=article_id, user=request.user, content=comment_content, parent_comment_id=pid)
    response_data["create_time"]=comment_obj.create_time.strftime("%Y-%m-%d")
    response_data["content"]=comment_obj.content
    response_data["username"]=comment_obj.user.username
    return JsonResponse(response_data)

#评论树
def comment_tree(request,article_id):
    ret = list(models.Comment.objects.filter(article_id=article_id).values("pk","content","parent_comment_id"))
    print(ret)
    return JsonResponse(ret,safe=False)


#后台管理 添加文章 backend_add_article.html
def add_article(request):

    if request.method=="POST":
        title=request.POST.get('title')
        article_content=request.POST.get('article_content')
        user=request.user

        from bs4 import BeautifulSoup

        bs=BeautifulSoup(article_content,"html.parser")
        desc=bs.text[0:150]+"..." #获取content纯文本内容，并切片为摘要


        # 过滤非法标签
        for tag in bs.find_all():
            print(tag.name)
            if tag.name in ["script", "link"]:
                tag.decompose()

        article_obj=models.Article.objects.create(user=user,title=title,desc=desc)
        models.ArticleDetail.objects.create(content=str(bs),article=article_obj) #为什么要用str 因为bs本身是个对象，使用str强转，执行对象中的 __str__方法


        return HttpResponse("添加成功")
    return render(request,"backend_add_article.html")


#接收富文本编辑器传过来的图片
from blog import settings
import os,json
def edit_upload(request):
    print(request.FILES)
    obj = request.FILES.get("upload_img") #在富文本编辑器中设置了filePostName:"upload_img"，类似form表单中 文件框的input name
    print("name",obj.name)

    path=os.path.join(settings.MEDIA_ROOT,"add_article_img",obj.name)  #设置保存路径为 media目录下的add_article_img
    with open(path,"wb") as f:
        for line in obj:
            f.write(line)
    res={
        "error":0,
        "url":"/media/add_article_img/"+obj.name
    }
    return HttpResponse(json.dumps(res))

#上传例子
@csrf_exempt
def upload(request):
    if request.method == "POST":
        file_obj = request.FILES.get("file_name")
        file_name = file_obj.name
        file_path = r"avatars/{}".format(file_name)
        with open(file_path,"wb") as f:
            for line in file_obj.chunks():
                f.write(line)
        return HttpResponse("上传成功")
    return render(request,"upload.html")

#验证码未封装版本
def check2(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20+40*i, 0), tmp, fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量，错误示例，应该保存到session
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    width = 220  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)

def test(request):
    return render(request,"2222222.html")
