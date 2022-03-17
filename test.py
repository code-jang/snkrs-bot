import json

Accounts = list()
account_info = dict()
Accounts.append(account_info)
account_info['name'] = 'name'
account_info["id"] = 'id'
account_info["password"] = 'password'

with open('./account_data.json', 'r') as fp:
    data = json.load(fp)

# data[0]['name'] = 'sana'

# with open('./account_data.json', 'r') as fp:
#     data = json.load(fp)

# with open('./account_data.json', 'w', encoding="utf-8") as FILE:
#     json.dump(Accounts, FILE, ensure_ascii=False, indent='\t')



