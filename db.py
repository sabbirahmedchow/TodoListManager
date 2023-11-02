from pymongo import MongoClient
from bson import ObjectId
from datetime import date

HOST = "mongo_db" #change the host based on docker container 
PORT = 27017

# Let us create a context manager for the database.
class DBConnect:
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.conn = None

    def __enter__(self):
        #print("Enter")
        self.conn = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #print("Exit")
        self.conn.close()


# This function is used to insert a single todo and update an existing todo 
# while adding back from the archive. Also, update a todo or todo date as per needed.
def save_todos(todo: str, todo_date: str, todo_id: str = None):
    with DBConnect(HOST, PORT) as c:
        p = c.conn.todos.todo
        checkIfExists = p.count_documents({"todo": todo})
        
        if checkIfExists == 0:
            if todo_id != None:
                delete_todo(todo_id, todo_date)
            p.insert_one({"todo": todo, "date": todo_date, "status": 1})
        else:
            print(todo_id)
            updateOpt = {"_id": ObjectId(todo_id)}
            changeTodo = {"$set": {"todo": todo, "date": todo_date, "status": 1}}  
            p.update_one(updateOpt, changeTodo)  
        
# This function is used to get the active todo list of the current date
def get_todo_list():
    with DBConnect(HOST, PORT) as c:
        p = c.conn.todos.todo
        date1 = str(date.today())
        list_todo = list(p.find({"date": date1, "status": 1}).sort([('$natural',-1)])) #get the latest/last item first
        return list_todo
    
# This function is used to update the status of a todo rather than deleting it. After updating, the list of 
# todos by date is returned ro regenerate the list.
def delete_todo(id: str, date: str):
    with DBConnect(HOST, PORT) as c:
        p = c.conn.todos.todo
        delOpt = {"_id": ObjectId(id)}
        changeStatus = {"$set": { "status": 0 }}
        p.update_one(delOpt, changeStatus)
        return get_datewise_todos(date)

# This function is used to get the archived todo list.
def get_archive_todos():
    with DBConnect(HOST, PORT) as c:
        p = c.conn.todos.todo
        arch_todo = list(p.find({"status": 0}).sort([('$natural',-1)]))
        return arch_todo     

# This function is used to get the datewise todo while selecting from the calender in todo list.
def get_datewise_todos(q):
    with DBConnect(HOST, PORT) as c:
        p = c.conn.todos.todo
        list_todo = list(p.find({"date": q, "status": 1}).sort([('$natural',-1)])) #get the latest item first
        return list_todo       




















