import socket

class Account:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_task_lists = []

    def get_user_id(self):
        return self.user_id
    
    def get_user_tasks(self):
        return self.user_task_lists

    def add_user_task_list(self, tl):
        self.user_task_lists.append(tl)
    
    def load_user_tasks_names(self):
        soc = socket.socket()
        soc.connect(self.server_data)
        soc.sendall(f"get_user_tasks_names {self.user_id}".encode())
        data = soc.recv(1024)
        data = data.decode()
        soc.close()
        return data

    def get_task_by_index(self, index):
        soc = socket.socket()
        soc.connect(self.server_data)
        soc.sendall(f"get_teacher_task_by_index {self.user_id}|{index}".encode())
        data = soc.recv(1024)
        data = data.decode()
        soc.close()
        return data