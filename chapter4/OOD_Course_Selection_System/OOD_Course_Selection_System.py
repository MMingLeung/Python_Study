#!/usr/bin/python
#-*- coding:utf8 -*-

import pickle
import time
'''
管理员：
        创建老师：姓名、性别、年龄、资产
        创建课程：课程名称、上课时间、课时费、关联老师
学生：
        用户名、密码、性别、年龄、选课列表[]、上课记录{课程1：【di,a,】}
    
    1. 管理员设置课程信息和老师信息
    2. 老师上课获得课时费
    3. 学生上课，学到“上课内容”
    4. 学生可自选课程
    5. 学生可查看已选课程和上课记录
    6. 学生可评价老师，差评老师要扣款
    7. 使用pickle
'''
FLAG = True
res = ''
class Manager:
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd

    def add_teacher(self):
        data = load_pickle('teacher_pi.txt')
        count = 1
        for i in data:
            count += 1
        new_teacher = input("Please input new teacher info:")
        new_teacher = eval(new_teacher)
        new_teacher["ID"] = count
        data.append(new_teacher)
        # print(data)
        data = pickle.dumps(data)
        write_file("teacher_pi.txt",data)
        data = load_pickle('teacher_pi.txt')
        print("现有老师信息如下: ",data)


    def add_course(self):
        data = load_pickle('course_pi.txt')
        count = 1
        for i in data:
            count += 1
        new_course = input("Please input new course info:")
        new_course = eval(new_course)
        new_course["ID"] = count
        data.append(new_course)
        data = pickle.dumps(data)
        write_file("course_pi.txt", data)
        data = load_pickle('course_pi.txt')
        print("现有课程信息如下: ",data)

    def exit(self):
        global FLAG
        FLAG = False
        return FLAG

class Teacher:
    def __init__(self, ID, name, sex, age, money, grade, password):
        self.ID = ID
        self.name = name
        self.sex = sex
        self.age = age
        self.money = money
        self.grade = grade
        self.password = password

    def teach_student(self):
        data = load_pickle("student_pi.txt")
        data_2 = load_pickle("course_pi.txt")
        for i_2 in range(len(data_2)):
            if self.name == data_2[i_2]["teacher"]:
                course_name = data_2[i_2]["name"]
                course_cost = data_2[i_2]["cost"]
                for i in range(len(data)):
                    if course_name in data[i]["course_list"]:
                        self.money += int(course_cost)
                        need_write = {"ID":self.ID,"name":self.name,"sex":self.sex,
                                      "age":self.age,"money":self.money,"grade":self.grade}
                        data_teacher = load_pickle("teacher_pi.txt")
                        for i_t in range(len(data_teacher)):
                            if self.ID == need_write["ID"]:
                                data_teacher[i_t] = need_write
                                #print(data_teacher[i_t])
                                print("课时费共有", need_write["money"])
                        data = pickle.dumps(data_teacher)
                        write_file("teacher_pi.txt", data)



    # def deduct_money(self):
    #     if self.grade <= "70":
    #         self.money -= 100
    #     elif self.grade <= "60":
    #         self.money -= 300
    #     elif self.grade <= "50":
    #         self.money -= 2000


class Student:
    def __init__(self, ID, username, password, sex, age, course, record):
        self.ID = ID
        self.username = username
        self.passwd = password
        self.sex = sex
        self.age = age
        self.course = course
        self.record = record
        self.data = load_pickle("student_pi.txt")

    def  attend_class(self):
        #上课
        for i in range(len(self.data)):
            if self.username == self.data[i]["name"]:
                course = self.data[i]["course_record"]
                # course.append("English")
                course_name = input("Please input course name:")
                course_status = input("Please input course record:")
                course[course_name]=course_status
        #print(self.data)
        res = pickle.dumps(self.data)
        write_file("student_pi.txt", res)


    def select_course(self):
        course_s = input("Please input course name: ")
        for i in range(len(self.data)):
            if self.username == self.data[i]["name"]:
                course = self.data[i]["course_list"]
                course.append(course_s)
                # for i in range(len(course)):
                #     print
                print("您报读课程如下: ",course)
        res = pickle.dumps(self.data)
        write_file("student_pi.txt",res)

    def check_course(self):
        course_record = self.data[0]["course_record"]
        course_list = self.data[0]["course_list"]
        print("Your course list:%s , Your course record:%s" % (course_list,course_record))


    def evaluate(self):
        course = input("Please input your course :")
        evaluate_level = input("Please input the course of teacher evaluation:(A,B,C(￥-300）,D（￥-800）)")
        data = load_pickle('course_pi.txt')
        # print(data)
        for i in range(len(data)):
            if course == data[i]["name"]:
                teacher_name = data[0]["teacher"]
                #print(teacher_name)
                data_2 = load_pickle('teacher_pi.txt')
                #print(data_2)
                for i in range(len(data_2)):
                    if data_2[i]["name"] == teacher_name:
                        if evaluate_level == "C":
                            data_2[i]["money"] -= 300
                        elif evaluate_level == "D":
                            data_2[i]["money"] -= 800
                        data_2[i]["money"] = str(data_2[i]["money"])
                print(data_2)
                res = pickle.dumps(data_2)
                write_file("teacher_pi.txt", res)





# class Course:
#     def __init__(self, ID, name, outline):
#         self.ID = ID
#         self.name = name
#         self.outline = outline



def read_file(filename):
    global res
    with open(filename, 'r') as file:
        for info in file:
            res += info
        return res


def write_file(filename,data):
    with open(filename, 'wb') as file:
        file.write(data)

def load_pickle(filename):
    with open(filename,'rb') as file:
        data = pickle.loads(file.read())
        return data

# def choice(identity,username,passwd):
#     if identity == 'manager':
#         manager = Manager(username,passwd)
#         data = load_pickle('manager_pi.txt')
#         # print(data)
#         if username == data["name"] and passwd == data["password"]:
#             while True:
#                 choice = input("Please input your choic: (add_teacher,add_course)")
#                 if not hasattr(manager, choice):
#                     print("Please input right choice")
#                 getmoth = getattr(manager, choice)
#                 return getmoth
#     elif identity == 'student':
#         pass
def choice(identity, username, passwd):
    if identity == "manager" and FLAG:
        data = load_pickle("manager_pi.txt")
        for i in range(len(data)):
            if data[i]["name"] == username and data[i]["password"] == passwd:
                manager = Manager(username, passwd)
                while True:
                    choice = input("Please input your choice :(add_teacher, add_course)")
                    if choice == 'exit':
                        break
                    method = getattr(manager, choice)
                    method()
    elif identity == "teacher" and FLAG:
        data = load_pickle("teacher_pi.txt")
        for i in range(len(data)):
            if data[i]["name"] == username and data[i]["password"] == passwd:

                manager = Teacher(data[i]["ID"], data[i]["name"], data[i]["sex"], data[i]["age"], data[i]["money"],
                                  data[i]["grade"], data[i]["password"])
                while True:
                    choice = input("Please input your choice :(teach_student)")
                    if choice == 'exit':
                        break
                    method = getattr(manager, choice)
                    method()

    elif identity == "student" and FLAG:
        data = load_pickle("student_pi.txt")
        for i in range(len(data)):
            if data[i]["name"] == username and data[i]["password"] == passwd:
                manager = Student(data[i]["ID"], data[i]["name"], data[i]["password"], data[i]["sex"], data[i]["age"],
                                  data[i]["course_list"], data[i]["course_record"])
                while True:
                    choice = input("Please input your choice :(attend_class, select_course, check_course, evaluate)")
                    if choice == 'exit':
                        break
                    method = getattr(manager, choice)
                    method()
    # if FLAG:
    #     file_path = identity+'_pi.txt'
    #     print(file_path)
    #     data = load_pickle(file_path)
    #     for i in range(len(data)):
    #         if data[i]["name"] == username and data[i]["password"] == passwd:
    #
    #             manager = Manager(username, passwd)
    #             while True:
    #                 choice = input("Please input your choice :(add_teacher, add_course)")
    #                 if choice == 'exit':
    #                     break
    #                 method = getattr(manager, choice)
    #                 method()

def run():
    while True:
        identity = input("Please input identity: (manager,teacher,student)")
        username = input("Please input username :")
        passwd = input("Please input password :")
        global FLAG
        FLAG = True
        choice(identity, username, passwd)
        # if identity == "manager" and FLAG :
        #     data = load_pickle("manager_pi.txt")
        #     for i in range(len(data)):
        #         if data[i]["name"] == username and data[i]["password"] == passwd:
        #             manager = Manager(username, passwd)
        #             while True:
        #                 choice = input("Please input your choice :(add_teacher, add_course)")
        #                 if choice == 'exit':
        #                     break
        #                 method = getattr(manager, choice)
        #                 method()




def transfer():
    # 转换为pickle
    res = [{"ID":1,"name":"Jack","password":"123","sex":"male","age":40,"money":1000,"grade":100}]
    res = pickle.dumps(res)
    write_file("teacher_pi.txt",res)
    data = load_pickle('teacher_pi.txt')
    print(data)



if __name__ == '__main__':
    run()
    # transfer()
    # data = load_pickle('teacher_pi.txt')
    # print(data)
    # a=data[0]["course_list"]
    # a.append("English")
    # for i in range(len(a)):
    #     print(a[i])
    #
    # m = Student(1,1,1,1,1,1,1,load_pickle('student_pi.txt'))
    # m.evaluate()





