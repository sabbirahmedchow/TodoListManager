from pymongo import MongoClient
from bson import ObjectId
from datetime import date

class DBConnect:
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.conn = None

    def __enter__(self):
        print("Enter")
        self.conn = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exit")
        self.conn.close()



def save_todos(todo: str, todo_date: str):
    with DBConnect("localhost", 27017) as c:
        p = c.conn.todos.todo
        p.insert_one({"todo": todo, "date": todo_date, "status": 1})
        
def get_todo_list():
    with DBConnect("localhost", 27017) as c:
        p = c.conn.todos.todo
        date1 = str(date.today())
        list_todo = list(p.find({"date": date1, "status": 1}).sort([('$natural',-1)])) #get the latest item first
        
        
        return list_todo
    
def delete_todo(id: str):
    with DBConnect("localhost", 27017) as c:
        p = c.conn.todos.todo
        delOpt = {"_id": ObjectId(id)}
        changeStatus = {"$set": { "status": 0 }}
        p.update_one(delOpt, changeStatus)

def get_archive_todos():
    with DBConnect("localhost", 27017) as c:
        p = c.conn.todos.todo
        arch_todo = list(p.find({"status": 0}))
        return arch_todo     

def get_datewise_todos(q):
    with DBConnect("localhost", 27017) as c:
        p = c.conn.todos.todo
        list_todo = list(p.find({"date": q, "status": 1}).sort([('$natural',-1)])) #get the latest item first
        return list_todo       




















