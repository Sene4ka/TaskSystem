import socket

class Account:
    def __init__(self, user_id, server_data):
        self.user_id = user_id
        self.user_task_lists = []
        self.server_data = server_data

    def get_user_id(self):
        return self.user_id
    
    def get_user_tasks(self):
        return self.user_task_lists

    def add_user_task_list(self, tl):
        self.user_task_lists.append(tl)
    
    def get_user_tasks_names(self):
        soc = socket.socket()
        soc.connect(self.server_data)
        soc.sendall(f"get_user_tasks_names {self.user_id}".encode())
        data = soc.recv(1024)
        data = data.decode()
        soc.close()
        return data if data != "nothing_found" else ""

    def get_task_by_name(self, name):
        soc = socket.socket()
        soc.connect(self.server_data)
        soc.sendall(f"get_teacher_task_by_name {self.user_id}|{name}".encode())
        data = soc.recv(1024)
        data = data.decode()
        soc.close()
        return data

    def delete_task_by_name(self, name):
        print(name)
        soc = socket.socket()
        soc.connect(self.server_data)
        soc.sendall(f"delete_task {self.user_id}|{name}".encode())
        soc.close()
        print(1)