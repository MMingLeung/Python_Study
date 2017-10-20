from bs4 import BeautifulSoup
def xss(old):
    valid_tag = {
        'p': ['class', 'id'],
        'img': ['src', 'alt'],
        'div': ['class'],
        'em': [''],
        'strong': [''],
    }
    soup = BeautifulSoup(old, "html.parser")
    tags = soup.findAll()
    for i in tags:
        if i.name not in valid_tag:
            # i.clear() #删除了内容
            i.decompose()  # 全部删除
        if i.attrs:
            for k in list(i.attrs.keys()):  # ['id', 'a']
                if k not in valid_tag[i.name]:
                    # 删除不合法的属性 直接删除key
                    del i.attrs[k]
    new_content = soup.decode()  # 对象 --> 字符串
    return new_content