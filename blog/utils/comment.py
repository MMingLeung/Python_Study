############## 打印 ##################
'''
1 
  2
3
  4
    5
'''
# comment_str = """"""
# """
# <div class='comment'>
#     <div class='content'>asd</div>
#     <div class='content'>asd</div>
#         <div class='comment'>
#         <div class='content'>asd</div>
#         <div class='content'>asd</div>
#         </div>
#     <div class='content'>asd</div>
# </div>
# """
#
# comment_str += "<div class='comment'>"
# for row in result:
#     tpl = "<div class='content'>%s</div>" % (row['content'])
#     comment_str += tpl
#     if row['child']:
#         comment_str += "<div class='comment'>"
#         for j in row['child']:
#             tpl = "<div class='content'>%s</div>" % (j['content'])
#             comment_str += tpl
#         comment_str += "</div>"
# comment_str += "</div>"

def comment_tree(result):
    '''
    
    :param result: [ {"id":'xx', ..}]
    :return: 
    '''
    comment_str = "<div class='comment'>"
    for row in result:
        tpl = "<div class='content'>%s</div>" % (row['content'])
        comment_str += tpl
        if row['child']:
            #comment_child干什么
            child_str = comment_tree(row['child'])
            comment_str += child_str
            comment_str += "</div>"
    comment_str += "</div>"
    print(comment_str)
    return comment_str
