import json

class Database:
    def insert(self,name,password,email,phno):
        with open('users.json','r') as rf:
            users=json.load(rf)
            if email in users:
                return 0
            else:
                users[email]=[name,password,phno]
        with open('users.json','w') as wf:
            json.dump(users,wf,indent=4)
            return 1
    def search(self,email,password):
        with open('users.json','r') as rf:
            users=json.load(rf)
            if email in users:
                if password==users[email][1]:
                    return 1
                else:
                    return 0
            else:
                return 0