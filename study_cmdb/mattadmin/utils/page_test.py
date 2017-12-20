class PageInfo:
    def __init__(self, current_page, all_count, base_url, page_param_dict, per_page=3, show_page=7):
        '''
        
        :param current_page:当前页码
        :param all_count: 数据总条数
        :param base_url: url
        :param page_param_dict: get请求参数 
        :param per_page: 每页显示条数
        :param show_page: 显示页码的数
        '''
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.all_count = all_count
        self.base_url = base_url
        self.page_param_dict = page_param_dict
        self.per_page = per_page
        self.show_page = show_page

        # 总条数/每页显示条数 = 多少页
        # 有余数要加多一页放置
        per_page_num, yu = divmod(self.all_count, self.per_page)
        if yu:
            per_page_num += 1
        self.all_page = per_page_num

    @property
    def start(self):
        # 一页10条数据 序号是0-9
        # 那么第二页就是从 (2 - 1)* 10 ---- 19
        return (self.current_page - 1) * self.per_page

    @property
    def stop(self):
        # 2 * 10 = 20 (ORM顾头不顾尾)
        return self.current_page * self.per_page

    def pager(self):
        page_list = []
        half = int((self.show_page - 1) / 2)

        # 总页数小于显示页码 all_page < show_page
        if self.all_page < self.show_page:
            start = 1
            stop = self.all_page + 1
        else:
            # 最小边界
            if self.current_page <= 5:
                start = 1
                stop = self.show_page + 1
            # 最大边界判定
            #
            else:
                if self.current_page + half > self.all_page:
                    # 15页是尽头，显示5页
                    # 15 - 5 = 11
                    # 15 + 1 = 16
                    start = self.all_page - self.show_page + 1
                    stop = self.all_page + 1
                else:
                    start = self.current_page - half
                    stop = self.current_page + half + 1

        if self.current_page <= 1:
            self.page_param_dict['page'] = 1
            pre = "<li><a href='{0}?{1}'>上一页</a></li>".format(self.base_url, self.page_param_dict.urlencode())
        else:
            self.page_param_dict['page'] = self.current_page - 1
            pre = "<li><a href='{0}?{1}'>上一页</a></li>".format(self.base_url, self.page_param_dict.urlencode())
        page_list.append(pre)

        for i in range(start, stop):
            self.page_param_dict['page'] = i
            if self.current_page == i:
                tmp = "<li class='active'><a href='{0}?{1}'>{2}</a></li>".format(self.base_url, self.page_param_dict.urlencode(), i)
            else:
                tmp = "<li><a href='{0}?{1}'>{2}</a></li>".format(self.base_url, self.page_param_dict.urlencode(), i)
            page_list.append(tmp)

        if self.current_page >= self.all_page:
            self.page_param_dict['page'] = self.all_page
            nex = "<li><a href='{0}?{1}'>下一页</a></li>".format(self.base_url, self.page_param_dict.urlencode())
        else:
            self.page_param_dict['page'] = self.current_page + 1
            nex = "<li><a href='{0}?{1}'>下一页</a></li>".format(self.base_url, self.page_param_dict.urlencode())
        page_list.append(nex)

        return ''.join(page_list)