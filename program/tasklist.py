import socket
from task import Task
import traceback
from PyQt5 import QtWidgets
import datetime

class TaskList:
    def __init__(self, name, server_data):
        self.server_data = server_data
        self.name = name
        self.type = ""
        self.tasks = []
        self.mark = 1
        self.marks_edges = [0.2, 0.4, 0.6, 0.8]
        self.last_answers = {}
        self.completed = False
        self.status = "Не выполнено"
        self.task_list_score = 0
        self.amount_completed = 0
        self.is_from_history = False

    def is_from_history_check(self):
        return self.is_from_history

    def add_task(self, task):
        self.tasks.append(task)

    def get_type(self):
        return self.type

    def on_run(self):
        self.status = "Выполняется"

    def set_type(self, type):
        self.type = type

    def get_name(self):
        return self.name

    def is_completed(self):
        return self.completed

    def get_user_answer(self, index):
        return self.tasks[index].get_user_answer()

    def on_complete(self):
        self.completed = True
        self.status = f"Выполнено, Балл: {self.task_list_score}"

    def get_status(self):
        return self.status

    def get_amount_of_completed(self):
        c = 0
        for i in self.tasks:
            if i.is_completed():
                c += 1
        return c

    def load_tasks(self, task_types):
        try:
            self.is_from_history = True
            for i in task_types.keys():
                to_send = f"get_data {i}"
                soc = socket.socket()
                soc.connect(self.server_data)
                soc.sendall(to_send.encode())
                data = soc.recv(2048)
                data = data.decode().split("|")
                soc.close()
                seeds = [j[0] for j in task_types[i]]
                user_answers = [j[1] for j in task_types[i]]
                print(seeds)
                soc = socket.socket()
                soc.connect(self.server_data)
                soc.sendall(f"get_task_data_from_seeds {i}|{';'.join(seeds)}".encode())
                data_t = soc.recv(2048)
                soc.close()
                data_t = data_t.decode().split("|")
                for j in range(len(data_t)):
                    data_l = data_t[j].split(";")
                    dt1 = data_l[0].split(":")
                    dt2 = data_l[1].split(":")
                    print(dt1, dt2)
                    #print(data, data_l)
                    #print(i, data[0], data[1], data[2], data[3], seeds[j], dt1, dt2, data_l[2])
                    task = Task(i, data[0], data[1], data[2], data[3], seeds[j], dt1, dt2, data_l[2])
                    #print(task)
                    task.set_preferred_parameters(user_answers[j])
                    self.tasks.append(task)
        except Exception:
            #print(Exception)
            #print(i, data[0], data[1], data[2], data[3], data_l[0], dt1, dt2, data_l[2])
            imsgBox = QtWidgets.QMessageBox()
            imsgBox.setIcon(QtWidgets.QMessageBox.Information)
            imsgBox.setText("Произошла непредвиденная ошибка.")
            imsgBox.setWindowTitle("Ошибка!")
            imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            imsgBox.exec()

    def form_tasks(self, task_types):
        try:
            for i in task_types.keys():
                soc = socket.socket()
                soc.connect(self.server_data)
                to_send = f"get_data {i}"
                soc.sendall(to_send.encode())
                data = soc.recv(2048)
                data = data.decode().split("|")
                soc.close()
                soc = socket.socket()
                soc.connect(self.server_data)
                to_send = f"get_seed {i}:{task_types[i]}"
                soc.sendall(to_send.encode())
                data_t = soc.recv(2048)
                data_t = data_t.decode().split("$")
                soc.close()
                for j in data_t:
                    data_l = j.split("|")
                    dt1 = data_l[1].split(";")
                    dt2 = data_l[2].split(";")
                    #print(data, data_l)
                    task = Task(i, data[0], data[1], data[2], data[3], data_l[0], dt1, dt2, data_l[3])
                    self.tasks.append(task)
        except Exception as e:
            #print(i, data[0], data[1], data[2], data[3], data_l[0], dt1, dt2, data_l[2])
            imsgBox = QtWidgets.QMessageBox()
            imsgBox.setIcon(QtWidgets.QMessageBox.Information)
            imsgBox.setText("Произошла непредвиденная ошибка.")
            imsgBox.setWindowTitle("Ошибка!")
            imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            imsgBox.exec()

    def on_task_complete(self, task_number, answer=None, check_only=False):
        if check_only:
            ans = self.tasks[task_number].on_task_complete(check_only=True)
        else:
            ans = self.tasks[task_number].on_task_complete(answer=answer)
            self.save_last_answer(str(task_number), answer)
        if ans[4]:
            self.task_list_score += int(ans[1])
        return ans[0], ans[1], ans[2], ans[3]

    def get_last_answer(self, task_number):
        if task_number in self.last_answers.keys():
            return self.last_answers[task_number]
        else:
            return ""

    def get_all_save_data(self):
        sl = {}
        rdata = []
        for i in self.tasks:
            dt = i.get_all_save_data().split(";")
            if dt[0] not in sl:
                sl[dt[0]] = [f"{dt[1]}:{dt[2]}"]
            else:
                sl[dt[0]].append(f"{dt[1]}:{dt[2]}")
        for i in sl.keys():
            rdata.append(f"{i};{';'.join(sl[i])}")
        mxb = 0
        b = self.task_list_score
        amc = 0
        at = len(self.tasks)
        for i in self.tasks:
            mxb += int(i.get_max_ball())
            if i.get_max_ball == i.get_score():
                amc += 1
        dole = b / mxb
        for i in self.marks_edges:
            if dole > i:
                self.mark += 1
        add_info = f"Выполнено: {amc}/{at}, Баллы: {b}/{mxb}, Оценка: {str(self.mark)}"
        date = datetime.datetime.now()
        date = date.strftime("%m/%d/%Y %H:%M")
        return f"{self.name}&{'|'.join(rdata)}&{add_info}&{date}"

    def send_mark_to_server(self):
        #soc = socket.socket()
        #soc.connect(())
        #soc.sendall(to_send.encode())
        #soc.close()
        pass

    def get_solution(self, n):
        return self.tasks[n].get_solution()

    def save_last_answer(self, task_number, value):
        self.last_answers[task_number] = value

    def get_right_answer(self, index):
        return self.tasks[index].get_answer()

    def get_task_score(self, index):
        return self.tasks[index].get_score()

    def get_score(self):
        return self.task_list_score

    def update_score(self):
        score = 0
        for i in self.tasks:
            score += int(i.get_score())
        self.task_list_score = str(score)
        print(self.task_list_score)


    def get_task_completeness(self, index):
        return self.tasks[index].is_completed()

    def get_user_task_answer(self, number):
        return self.tasks[number].get_user_answer()

    def get_amount_of_tasks(self):
        return len(self.tasks)

    def in_list(self, task):
        f = False
        for i in self.tasks:
            if i.get_class_id() == task.get_class_id():
                f = True
        return f
    
    def get_seeds(self):
        f = []
        for i in self.tasks:
            if i.get_seed() != "":
                f.append(i.get_seed())
        return f

    def get_task_by_number(self, position, get_only_text=False, get_only_name=False):
        try:
            task = self.tasks[position]
            if get_only_text:
                return task.get_text()
            elif get_only_name:
                return task.get_name()
            return task
        except IndexError:
            return "no_task"


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text) 
        
        
        
        
        
