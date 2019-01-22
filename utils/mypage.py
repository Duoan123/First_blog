#!/usr/bin/env python
#-*-coding=utf-8 -*-
#GKX

class Page():
    def __init__(self,page_num,total_count,url_prefix,per_page=10,max_page=11):
        """
        用于html页面的分页
        :param page_num:    当前页码数
        :param total_count: 数据总页码数
        :param url_prefix:  a标签href的前缀
        :param per_page:    每页显示多少条数据
        :param max_page:    页面上最多显示几个页码
        """
        self.url_prefix = url_prefix
        self.max_page = max_page
        # 每一页显示多少条数据
        # 总共需要多少页码来展示
        total_page,m = divmod(total_count,per_page)             #total_count和per_page只需要在__init__中使用，后面的方法调用不到，因此不用传入self
        if m or (total_page==0 and m==0) :
            total_page +=1
        # if not (m or total_page): #当m和total_page同时为0，也就是数据库为空的时候，给总页码赋值为1
        #     total_page += 1
        self.total_page = total_page                            #把总页码传入self

        try:
            page_num = int(page_num)
            # 如果输入的页码数超过了最大的页码数，默认返回最后一页
            if page_num > self.total_page:
                page_num = self.total_page
        except Exception as e:
            # 当输入的页码不是正经数字的时候 默认返回第一页的数据
            page_num = 1
        self.page_num = page_num                                #把page_num传入self

        # 定义两个变量保存数据从哪儿取到哪儿
        self.data_start = (page_num-1)*per_page
        self.data_end = page_num*per_page

        #页面上总共展示多少代码
        if self.total_page < self.max_page:
            self.max_page = self.total_page

        half_max_page = self.max_page // 2
        #页面上的页码开始的位置 和 结束的位置
        page_start = page_num - half_max_page
        page_end = page_num + half_max_page

        if page_start <= 1:
            page_start = 1
            page_end = self.max_page
        if page_end >= self.total_page:
            page_end = self.total_page
            page_start = self.total_page - self.max_page + 1

        self.page_start = page_start   #当page_start判断完毕后，才传入self。对于那些直接在__init__一开始就传入self的来说，实例化的属性就是传入的值，不存在需要判断的，所以可以直接传入
        self.page_end = page_end       #但是此时page_start和page_end需要传入参数后，再做一定的判断才能确定下来，确定后才能传给self，方便方法中调用

    @property
    def start(self):
        return self.data_start

    @property
    def end(self):
        return self.data_end

    def page_html(self):
        #自己拼接分页的HTML代码
        html_str_list = []
        #首页按钮
        html_str_list.append('<li><a href="{}?page=1">首页</a></li>'.format(self.url_prefix))

        #判断一下 如果是第一页，就没有上一页
        if self.page_num <=1 :
            html_str_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            html_str_list.append('<li><a href="{}?page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.url_prefix,self.page_num-1))

        for i in range(self.page_start,self.page_end+1):
            if i == self.page_num:
                tmp = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix,i)
            else:
                tmp = '<li><a href="{0}?page={1}">{1}</a></li>'.format(self.url_prefix,i)
            html_str_list.append(tmp)
        # 加一个下一页的按钮
        # 判断，如果是最后一页，就没有下一页
        if self.page_num >= self.total_page:
            html_str_list.append(
                '<li class="disabled"><a href="#"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_str_list.append(
                '<li><a href="{}?page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.url_prefix,self.page_num + 1))
        # 加最后一页
        html_str_list.append('<li><a href="{}?page={}">尾页</a></li>'.format(self.url_prefix, self.total_page))

        page_html = "".join(html_str_list)
        return page_html

















