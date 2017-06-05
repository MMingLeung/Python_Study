
# coding: utf-8

# # 练习题：
# 1. 使用while循环输入 1 2 3 ... 8 9 10

# In[2]:

i = 0
while i <= 100:
    print (i)
    i += 1


# 2. 求1-100的所有数的和

# In[3]:

i = 0
count = 0
for i in range(101):
    count += i
print (count)


# 3. 输出 1-100 内的所有奇数

# In[4]:

i = 0
count = 0
for i in range(101):
    if i % 2 != 0:
        count += i
print (count)


# 4. 输出 1-100 内的所有偶数

# In[5]:

i = 0
count = 0
for i in range(101):
    if i % 2 == 0:
        #print (i)
        count += i
print (count)


# 5. 求1-2+3-4 ... 99的所有数的和

# In[6]:

i = 0
count = 0
for i in range(100):
    if i % 2 == 0:
        #print (i)
        count -= i
    else:count +=i
print (count)


# # 模拟登陆
# 1. 用户输入帐号密码进行登陆
# 2. 用户信息保存在文件内
# 3. 用户密码输入错误三次后锁定用户

# In[1]:

print ('====Login Program====')
with open('account.txt','r') as file_read:
    file = file_read.read()
    data = eval(file)
    while data['count'] < 3 and not data['lock'] :
        username_input = input("please input email: ")
        passwd_input = input("please input password: ")
        if username_input == data['username']  and passwd_input == data['passwd']:
            print('weclome !')
        else:
            data['count'] += 1
            print("your email or passwd is invalid")
    else:
        print('Your account has been locked')
        with open('account.txt', 'r') as file_read:
            file_lines = file_read.readlines()
        with open('account.txt','w') as file_write:
            for line in file_lines:
                if 'lock' in line:
                    file_write.write(line.replace('\'lock\':0','\'lock\':1'))
                else:
                    file_write.write(line)


# # 三级菜单：
# 1. 运行程序输出第一级菜单
# 2. 选择一级菜单某项，输出二级菜单，同理输出三级菜单
# 3. 返回上一级菜单和顶部菜单
# 4. 菜单数据保存在文件中

# In[2]:

file = open("city.txt",'r',encoding='utf-8')    # 打开文本文件
f = file.read()
file_str=str(f) # 将每行信息转成字符串格式
data = eval(file_str)    # 字符串转成字典格式
#print (data)

last_layers = [data]
current_layer = data

while True:
    for key in current_layer:
        print(key)
    choice = input('Please input: ').strip()
    if len(choice) == 0 : continue
    elif choice == 'b':
        current_layer = last_layers[-1]
        last_layers.pop() #删除最后一个
    elif choice == 'q':
        break
    if choice in current_layer :
        last_layers.append(current_layer)
        current_layer = current_layer[choice]


# # 购物车
# 1. 商品信息- 数量、单价、名称
# 2. 用户信息- 帐号、密码、余额
# 3. 用户可充值(#目前程序只能退出之后,下一次进入才能查询正确的金额)
# 4. 购物历史信息
# 5. 允许用户多次购买，每次可购买多件
# 6. 余额不足时进行提醒
# 7. 用户退出时 ，输出档次购物信息
# 8. 用户下次登陆时可查看购物历史
# 9. 商品列表分级(此项没有完成)

# In[2]:

print('=====shopping cart program in python=====')

product_list = [['xiaomi',1999],
                ['iphone7',6599],
                ['iphone7-plus',7999],
                ['huawei-mate7',3999],
                ['yijia',2000],
                ['chuizi',2999]
                ]

#用户登录信息
#读取用户信息文件
with open('shopping_cart_accounts.txt','r') as file:
    total_price = 0
    shopping_cart ={}
    the_rest_of_money = 0
    f = file.read()
    data = eval(f)    # 字符串转成字典格式
    Msg = '''Your balance of account is: {money}
          '''
    while True:
        email = input("Please input your email: ")
        passwd = input("Please input your passwd: ")
        if email == data['email'] and passwd == data['passwd'] :
            print (Msg.format(money=data['money']))
            break

    while True:

        index = 1
        for product in product_list:

            print(index,':',product)
            index +=1

        choice = input("please input your buy").strip()

        if choice.isdigit(): #判断是否是数字
            choice = int(choice)-1
            if choice >= 0 and choice < len(product_list) :#商品存在
                product = product_list[choice]
                if product[1] <= data['money']:
                    if product[0] in shopping_cart:
                        shopping_cart[product[0]][1] += 1
                        data['buy_history'] = shopping_cart
                        print(data['buy_history'])
                        print(product[0])
                    else:
                        shopping_cart[product[0]] = [product[1],1]#[price , quantity]
                        data['buy_history'] = shopping_cart
                        print(data['buy_history'])
                        data['money'] -= product[1]
                    print("Added product" + '  '+ product[0] + ' ' +
                          "into shopping cart ,\033[42;1myour current balance\033[0m :"+str(data['money']))
                else:
                    print("you haven't enough money, product price is:" + '  '+
                           str(product[1]) +'  '+ "you need more money" + '  '+
                           str(product[1] - data['money']))
            else:
                print("Production isn't exist")

        elif choice == 'h':
            with open("G:\\untitled\\buy_history.txt") as f:
                msg = '''==========Shopping History(except this time)==========
    name          price        quantity'''
                print(msg)
                for line in f:
                    print (line)

        elif choice == 'info':
            print('Your email is %s, your password is %s, your money are %s' %
                    (data['email'], data['passwd'],data['money']))

        elif choice == 'charge':
            money = int(input("Please input money "))
            with open('G:\\untitled\\shopping_cart_accounts.txt', 'r') as f_read:
                lines = f_read.readlines()
            with open('G:\\untitled\\shopping_cart_accounts.txt', 'w') as f_write:
                for line in lines:
                    if "money" in line:
                        f_write.write("\'money\':"+str(money+data['money'])+'\n')
                    else:
                        f_write.write(line)

        elif choice == 'q' :
            print("===============your have brought===============")
            print("id    production    quantity    price    total")
            index = 1
            # for key in data['buy_history']:
            #     print(key)
            for key in shopping_cart:

                print("%d %10s %10d %10d %10d" %(
                       index,
                       key,
                       shopping_cart[key][1],
                       shopping_cart[key][0],
                       shopping_cart[key][0] * shopping_cart[key][1]))
                index +=1
                total_price += shopping_cart[key][0] * shopping_cart[key][1]
            print("total :", total_price)
            print("your balance is",data['money'])
            print("shopping end")
            break


        else :
            print("No this choice")

    with open('G:\\untitled\\buy_history.txt','a') as f_read:
        for key in shopping_cart:
            f_read.write("%s %10d %10d\n"
                    %(key,shopping_cart[key][0], shopping_cart[key][1]))


# In[ ]:



