#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado.web import UIModule


class UserUIModule(UIModule):
    '''
    处理前端好友信息
    '''
    def render(self, friends, my_data, *args, **kwargs):

        friends_list_tpl = """
        <div my_id={my_id} my_name={my_name}>
        {friends}
        </div>
        """
        friend_info_tpl = """
        <div nid={nid} name={origin}>
        <span>好友ID: {id}</span> | 昵称: <span>{name}</span><button onclick='connectServer(this)'>会话</button>
        </div>
        """
        friends_info_result = ""
        for friend in friends:
            friends_info_result += friend_info_tpl.format(id=friend[0], name=friend[1], nid=friend[0], origin=friend[1])
        friends_list_tpl = friends_list_tpl.format(friends=friends_info_result, my_id=my_data[0], my_name=my_data[1])
        return friends_list_tpl


class ApplyMsgUIModule(UIModule):
    '''
    处理前端好友申请信息
    '''
    def render(self, apply_data, *args, **kwargs):
        tpl = "<div><form method='POST' action='/add_friend'>{content}</form></div>"
        tmp = ""
        for data in apply_data:
            temp_tpl = "<div>" \
                       "<span>{username}</span> 的好友申请 " \
                       "<input style='display: none;' name=user_apply value={user_apply}>" \
                       "<input type='submit' value='确认'>" \
                       "</div>"
            tmp += temp_tpl.format(username=data['username'], user_apply=data['user_apply'])
        return tpl.format(content=tmp)


class UserGoupUIModule(UIModule):
    '''
    处理前端用户组信息
    '''
    def render(self, group_data, my_data, *args, **kwargs):
        print('my_data', my_data)
        outer_tpl = "<div my_id={my_id} my_name={my_name}>{content}</div>"
        group_tpl = """
                    <div gid={gid} gname={group_name} id=group_{gid}>
                        <span>组ID: {gid}</span> | 组名: <span>{group_name}</span>
                        <button onclick='showMem(this), connectGServer(this)'>会话</button>
                    </div>
                    """
        result_tpl = ""
        for group in group_data:
            result_tpl += group_tpl.format(gid=group['gid'], group_name=group['gname'])
        return outer_tpl.format(content=result_tpl,my_id=my_data[0], my_name=my_data[1] )
