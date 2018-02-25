import json
# def write():
#     data = [{'username':"Jack", "password":'123', "quota":'5m'}]
#     data = json.dumps(data)
#     with open('accounts.json', 'w') as file:
#         file.write(data)

def load_w():
    with open("accounts.json", 'r') as file:
        f = file.read()
        data = json.loads(f)
        data.append({'username':"Tom", "password":'123', "quota":'5m'})
        data = json.dumps(data)
        with open("accounts.json", 'w') as f:
            f.write(data)


# write()
# data = load()
# print(type(data ))

def load():
    with open("accounts.json", 'r') as file:
        f = file.read()
        data = json.loads(f)
        print(data)
load()