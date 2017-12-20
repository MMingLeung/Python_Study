class PageInfo:
    '''
    current_page:当前点击的页码
    per_page：每页显示的数据数量    
    all_count：数据总共的数量
    base_url：网页根地址
    show_page：页码总共显示的个数
    page_param_dict: url原参数
    '''
    def __init__(self, current_page, per_page, all_count, base_url, page_param_dict,show_page=11):
        print('allcount', all_count)
        try:
            #当前页转换为int
            self.current_page =int(current_page)
        except Exception as e :
            self.current_page = 1
        self.per_page = per_page
        self.all_count = all_count
        self.base_url = base_url
        self.page_param_dict = page_param_dict
        #计算总共的页码数
        #a 是商，b是余数，余数大于1需要增加一页放置
        a, b = divmod(self.all_count, per_page)
        if b:
            a += 1
            #总页数
        self.all_page = a
        self.show_page = show_page

    @property
    def start(self):
        #数据开始的序号，比如我点击第一页，数据开始位置是0
        return (self.current_page-1) * self.per_page

    @property
    def stop(self):
        # 数据结束的序号，比如我点击第一页，数据结束位置是10 ， 0-10显示10条
        return self.current_page * self.per_page


    def pager(self):
        #建立列表存放计算得出的数据序号
        page_list = []
        #显示页码的一半 -1 2 3 4 5-6-7 8 9 10 11- 显示11条，左右各5条
        half = int((self.show_page - 1) / 2)
        #( 11 - 1 )/ 2 = 5


        print(self.all_count)

        # 如果数据总页数 < 11 , 只显示现有数据的总页数，就是all_page
        # 开始页数永远等于1 ， 结束页码就是最大页数
        if self.all_page < self.show_page:
            start = 1
            end = self.all_page + 1
        else:
            #总页数大于11

            #如果我点击12345永远显示前11页，当前页为1， 结束页等于show_page
            if self.current_page <= 5:
                start = 1
                end = self.show_page + 1
            else :
                #如何点击的页码+  后5页 > 总共页数，对极限值做判断， 后面的页码不需要增加
                if self.current_page + half > self.all_page:
                    #最后一页往前面数，减去show_page + 1
                    # 20 - 11 = 9 + 1
                    # 21
                    start = self.all_page - self.show_page + 1
                    end = self.all_page + 1
                else:
                    #当前页往前5页，和往后5页（开始的问题，会出现负数，所以要加判断）
                    start = self.current_page - half
                    end = self.current_page + half +1


        if self.current_page <= 1:
            prev = " <li><a href='%s?page=#'>上一页</a></li>" % (self.base_url)
        else:
            self.page_param_dict['page'] = self.current_page - 1
            prev = " <li><a href='%s?%s'>上一页</a></li>" % (self.base_url, self.page_param_dict.urlencode(), )

        page_list.append(prev)


        for i in range(start, end):
            self.page_param_dict['page'] = i
            if i == self.current_page:
                temp = " <li class='active'><a href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(),i,)
            else:
               temp = " <li><a href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(),i,)
            page_list.append(temp)


        if self.current_page >= self.all_page:
            nex = " <li><a href='%s?%s'>下一页</a></li>" % (self.base_url, self.page_param_dict.urlencode(),)
        else:
            nex = " <li><a href='%s?%s'>下一页</a></li>" % (
            self.base_url, self.page_param_dict.urlencode(),)

        page_list.append(nex)

        page_list = ''.join(page_list)
        return page_list
