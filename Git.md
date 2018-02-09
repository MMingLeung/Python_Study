# GitHub

## 单机模式

### 流程

1. 进入程序目录
2. git init                            # 初始化
3. git status                      # 查看 git 状态 
4. git add .                        # 把当前目录文件提交到 git 暂存区中
5. git commit -m '描述'   # 把暂存区文件提交到分支并添加描述

<br>

*配置 username、email:*

*git config —local user.name 'Matt'*

*git config —local user.email 'Matt@gmial.com'* 

<br>

6. git log                               # 查看历史记录

### Git 管理区图示

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/git/git_01.png?raw=true)



<br>

### 版本回溯

1. git log                               # 查看历史记录，查看版本号
2. git reset —hard 版本号 # 回溯到该版本提交之前的内容

<br>

### Git 管理区图示

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/git/git_02.png?raw=true)

<br>

## 分支系统

### 使用

1. git branch branch_name                                   # 创建分支
2. git checkout branch_name                                # 切换分支
3. 在分支中开发
4. git add . ;git commit -m 'msg'
5. git checkout master                                            # 切换回主分支
6. git merge dev                                                       # 把分支内容合并到主分支
7. git branch -D branch_name                               # 删除分支

<br>

## 远程仓库及协同开发

### 流程

**PC_1:**

1. GitHub                                                # 创建仓库
2. 进入本地文件目录 git init 初始化
3. git remote add url                            # 添加远程仓库
4. git add .                                              # 添加文件到暂存区
5. git commit -m 'msg'                         # 把文件提交到分支
6. git push origin master                    # 把文件提交到远程仓库 master 分支

>第6步需要填写账号密码，无密码方式
>
>​    1、生成公钥ssh-keygen
>
>​    2、cat ~/.ssh/id_rsa.pub公钥复制到git上 （头像->setting->ssh）
>
>​    3、git clone ssh地址

7. git push origin dev                           # dev 分支文件推送

<br>

**PC_2:**

1. git clone url                                       # 从 GitHub 中下载文件
2. git branch dev origin/dev               # 下载 dev (或其它分支)到本地
3. 开发新功能 & add & commit
4. git push origin dev

<br>

**PC_1:**

1. git pull origin dev                             # 从 GitHub 中下载最新文件
2. 开发新功能 & add & commit  & push  

<br>

**PC_2:**

1. git fetch origin dev                           # dev 分支下，把远程仓库最新内容下载到版本区
2. git merge origin/dev                        # 把最新内容合并到工作区
3. 开发 & add & commit









