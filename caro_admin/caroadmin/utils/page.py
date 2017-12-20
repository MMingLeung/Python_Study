from django.utils.safestring import mark_safe


class PageInfo(object):
    '''
    自定义分页
    '''
    def __init__(self, all_count, current_page, param_dict, path_info,per_page=3, show_page=7):
        '''
        
        :param all_count: 数据总数量
        :param current_page: 当前页码
        :param param_dict: 当前url get请求的参数（QueryDict）
        :param path_info: 当前url
        :param per_page: 每页显示的数量
        :param show_page: 显示的页码数量
        '''
        self.all_count = all_count
        self.param_dict = param_dict
        self.path_info = path_info
        self.per_page = per_page
        self.show_page = show_page

        if not current_page:
            self.current_page = 1
        else:
            self.current_page = int(current_page)

        # 计算需要的页数（总页数）
        a,b = divmod(self.all_count, self.per_page)
        if b:
            a += 1
        self.all_page = a

    @property
    def start(self):
        '''  
        获取数据的开始索引
        比如：per_page = 3
             现在显示第二页，第二页的第一条数据索引是3
             ( 2 - 1 ) * 3
        :return: 索引
        '''
        return (self.current_page - 1) * self.per_page

    @property
    def stop(self):
        '''
        获取数据的结束索引
        比如：per_page = 3 
             现在显示第二页，第二页的第最后条数据索引是6
             2 * 6
        :return: 
        '''
        return self.current_page * self.per_page

    def pager(self):
        # 存放html标签
        show_list = []

        # half
        half = int((self.per_page-1)/ 2)

        # 判断各项极限值
        if self.all_page < self.show_page:
            # 如果总页数小于显示的页数
            start = 1
            stop = self.all_page + 1
        else:
            if self.current_page < half:
                # 左峰值
                start = 1
                stop = self.show_page + 1
            else:
                if self.current_page + half > self.all_page:
                    # 右峰值
                    # show_page = 3
                    # all_page = 10
                    # start = 7 + 1 stop = 10 + 1
                    start = self.all_page - self.show_page + 1
                    stop = self.all_page + 1
                else:
                    start = self.current_page + 1
                    stop = self.current_page + self.per_page + 1

        # 上一页
        if self.current_page == 1:
            self.param_dict['page'] = 1
            pre = "<li><a href='{}?{}'>上一页</a></li>".format(self.path_info, self.param_dict.urlencode())
        else:
            self.param_dict['page'] = self.current_page - 1
            pre = "<li><a href='{}?{}'>上一页</a></li>".format(self.path_info, self.param_dict.urlencode())
        show_list.append(pre)

        print(start, stop)
        for _ in range(start, stop):
            self.param_dict['page'] = _
            if self.current_page == _:
                tpl = "<li><a href='{}?{}' class='active'>{}</a></li>".format(self.path_info, self.param_dict.urlencode(), _)
            else:
                tpl = "<li><a href='{}?{}' class='active'>{}</a></li>".format(self.path_info, self.param_dict.urlencode(), _)
            show_list.append(tpl)

        # 下一页
        if self.current_page == self.all_page:
            self.param_dict['page'] = self.all_page
            pre = "<li><a href='{}?{}'>下一页</a></li>".format(self.path_info, self.param_dict.urlencode())
        else:
            self.param_dict['page'] = self.current_page + 1
            pre = "<li><a href='{}?{}'>下一页</a></li>".format(self.path_info, self.param_dict.urlencode())
        show_list.append(pre)
        return mark_safe(''.join(show_list))