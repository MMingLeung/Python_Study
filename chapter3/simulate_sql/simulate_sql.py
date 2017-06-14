#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
仿SQL程序
1、可进行模糊查询，语法至少支持下面3种:
    select name,age from staff_table where age > 35
    select  * from staff_table where dept = "技术"
    select  * from staff_table where enroll_date like "2019"
2、查到的信息，打印后，最后面还要显示查到的条数 
3、可创建新员工纪录，以phone做唯一键，staff_id需自增
4、可删除指定员工信息纪录，输入员工id，即可删除
5、可修改员工信息，语法如下:
　　UPDATE staff_table SET dept="Market" WHERE where dept = "IT"

'''
res = []
def file_object():
    with open('data.txt','r+') as file:
        for line in file:
            res.append(line.split(','))
        return res

def file_object_write(need_write):
    with open('data.txt','w') as file:
        file.write(need_write)

def search_info(res):
    select_all = False
    # 把data.txt中的数据转换成字典形式
    data_list = ({'No': line[0], 'name': line[1], 'age': line[2], 'phone': line[3], 'dept': line[4],
                  'enroll_date': line[5].strip()} for line in res)
    user_input = input('Please input your search statement: ')
    # 以下4条search是对用户输入的语句进行切分，获取关键词
    if 'where' in  user_input:
        search_info = user_input.split()[1]
        search_key = user_input.split()[-3]
        search_symbol = user_input.split()[-2]
        search_comparison = user_input.split()[-1]
        if "\"" in search_comparison:
            search_comparison = search_comparison[1:-1]
        print(search_comparison)
        #print(search_info,search_key,search_symbol,search_comparison)
    # 截取select name,age from staff_table where age > 35：name,age age > 35
    else:
        search_info = user_input.split()[1]
        select_all = True
        search_symbol=''
        search_comparison=''
        search_key=''
    # '*'的设置
    if search_info == '*':
        search_info = 'No,name,age,phone,dept,enroll_date'
    # 拆分select name,age from file where age > 30 中的name,age等词
    search_info_list = search_info.split(',')
    # 用于circulate_info_list()函数
    info_key = ''
    info_list = []
    # 计数器，用于记录有多少条记录
    count = 1
    #if search_comparison == '' and search_symbol == '' and search_where == '':

    for line in data_list:
        if search_symbol == '=' and not select_all:
            if line[search_key] == search_comparison:
                info_list, count = circulate_info_list(search_info_list, info_key, info_list, line, count)
        elif search_symbol == 'like'and not select_all:
            if search_comparison in line[search_key]:
                info_list, count = circulate_info_list(search_info_list, info_key, info_list, line, count)
        elif select_all:
            info_list, count = circulate_info_list(search_info_list, info_key, info_list, line, count)
        else:
            chaxunyuju = line[search_key] + ' ' + search_symbol + ' ' + search_comparison
            if eval(chaxunyuju) and not select_all:
                info_list, count = circulate_info_list(search_info_list, info_key, info_list, line, count)

    print(info_list, 'total: ' + str(count - 1))

def circulate_info_list(search_info_list,info_key,info_list,line,count):
    '从search_info拆分的词语，把其作为key，获得value，拼接后返回'
    for info in search_info_list:
        info_key += '   ' + line[info]
    info_list.append(str(count) + info_key)
    info_key = ''
    count += 1
    return  (info_list,count)

def add_info(res):
    '实现仿SQL中添加语句查询'
    data_list = ({'No': line[0], 'name': line[1], 'age': line[2], 'phone': line[3], 'dept': line[4],
                  'enroll_date': line[5].strip()} for line in res)
    # for i in data_list:
    #     print(i['phone'])
    person_info = input("Please input add infomation statement about name,age,phone_number,dept,enroll_date: ")
    # 切分用户输入的人员信息
    person_res = person_info.split(',')
    person_info_dict = {'name': person_res[0], 'age': person_res[1], 'phone': person_res[2], 'dept': person_res[3],
                        'enroll_date': person_res[4]}
    line_no = 0
    for line in res:
        line_no += 1
    line_count = 0
    for line in data_list:
        # print(person_info_dict['phone'],line['phone'])
        # 判断'phone'是否有重复，没有则在末端写入
        line_count += 1
        if person_info_dict['phone'] == line['phone'] :
                break
        if line_count == line_no :
            person_info = (str(int(line['No'])+1)+','+person_info+'\n').split(',')
            res.append(person_info)
    need_write=''
    for i in res:
        need_write += ','.join(i)
    file_object_write(need_write)

def delete_info(res):
    '实现仿SQL中删除语句查询'

    id = input("Please input delete id :")
    need_write = ''
    for line in res:
        if id == line[0]:
            line =''
        need_write += ','.join(line)
    file_object_write(need_write)

def update_info(res):
    '实现仿SQL中修改语句查询'
    data_list = ({'No': line[0], 'name': line[1], 'age': line[2], 'phone': line[3], 'dept': line[4],
                   'enroll_date': line[5].strip()} for line in res)

    user_input = input("Please input update statement :")
    search_info = user_input.split()[3]
    search_key = user_input.split()[-3]
    search_comparison = user_input.split()[-1]
    search_comparison = search_comparison[1:-1]
    #截取UPDATE staff_table SET dept="Market" WHERE where dept = "IT" ：dept="Market" dept IT
    #print(search_info,search_key,search_comparison.strip())
    g = [l for l in search_info.split('=')]
    g[1] = g[1][1:-1]
    need_write =''
    for line in data_list:
        if line[search_key] == search_comparison:
            line[search_key] = g[1]
        msg = '''{No},{name},{age},{phone},{dept},{enroll_date}\n'''
        a = (msg.format(No=line['No'],name=line['name'],age=line['age'],phone=line['phone'],dept=line['dept'],
                         enroll_date=line['enroll_date']))
        need_write += a
    file_object_write(need_write)

cmd_dic = {
    'search':search_info,
    'add':add_info,
    'update':update_info,
    'delete':delete_info,
    'exit':quit,
}

def tell_msg():
    msg = '''
    search:查询
    add:添加
    update:更改
    delete:删除
    exit:退出
    '''
    print(msg)

while True:
    tell_msg()
    choice = input('Please input your choice: ')
    cmd_dic[choice]()




