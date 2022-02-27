import sys
import traceback
import socket
from PyQt5 import QtWidgets
from design import Ui_MainWindow
from tasklist import TaskList
from account import Account


class Program(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.account = None
        self.user_id = "1"
        self.self_task_lists = []
        self.user_task_lists = []
        self.current_task_list = None
        self.current_task_list_number = -1
        self.current_task_number = -1
        self.task_select_items = {}
        self.no_name = 0
        self.current_item = -1
        self.allowed_letters = "qwertyuiopasdfghjklzxcvbnm_ёйцукенгшщзхъфывапролджэячсмитьбю"
        self.allowed_numbers = "0123456789"
        self.setWindowTitle("Генератор задач")
        self.solution_base_text = "После отправки ответа здесь будет показано решение."
        self.task_solution.setText(self.solution_base_text)
        self.task_solution.setReadOnly(True)
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabVisible(2, False)
        self.tabWidget.setCurrentIndex(1)
        #self.tabWidget.setTabEnabled(3, False)
        #self.task_history.setCurrentRow(1)
        self.task_choose.activated.connect(lambda: self.choose_task())
        self.send_btn.clicked.connect(lambda: self.check_answer())
        self.end_work.clicked.connect(lambda: self.end_task())
        self.self_tl.itemClicked.connect(self.on_self_task_list_choice)
        self.self_tl.itemClicked.connect(self.on_self_task_list_choice)
        self.tabWidget.currentChanged.connect(self.update_lists)
        self.add_task.clicked.connect(lambda: self.go_to_task_list_creation())
        self.cancel.clicked.connect(lambda: self.cancel_pressed())
        self.save.clicked.connect(lambda: self.save_pressed())
        self.btn_plus.clicked.connect(lambda: self.add_item())
        self.btn_minus.clicked.connect(lambda: self.remove_item())
        self.task_history.itemClicked.connect(self.load_task_from_history)
        self.tl_name.textChanged.connect(self.check_tl_text)
        self.answer_edit.textChanged.connect(self.check_answer_field)

    def login(self, username, password):
        user_id = None # sql connect
        self.account = Account(user_id)

    def check_tl_text(self):
        text = list(self.tl_name.text())
        n_text = []
        for i in text:
            if i in self.allowed_letters or i in self.allowed_numbers:
                n_text.append(i)
        self.tl_name.setText("".join(n_text))

    def check_answer_field(self):
        text = list(self.answer_edit.text())
        n_text = []
        for i in text:
            if i in self.allowed_numbers:
                n_text.append(i)
        self.answer_edit.setText("".join(n_text))

    def create_self_task_list(self, name, tasks={}):
        tl = self.create_task_list(name, tasks)
        self.self_task_lists.append(tl)
        self.form_self_task_lists()

    def check_answer(self, check_only=False):
        answer = self.answer_edit.text()
        ans = self.current_task_list.on_task_complete(self.current_task_number, answer=answer, check_only=check_only)
        if ans[3]:
            self.label_tmp_1.clear()
            self.label_tmp_1.hide()
            self.answer_edit.clear()
            self.answer_edit.setReadOnly(False)
            self.answer_edit.setText(self.current_task_list.get_last_answer(str(self.current_task_number)))
            self.send_btn.show()
            self.task_solution.setText(self.solution_base_text)
        else:
            self.task_solution.setText(self.current_task_list.get_solution(self.current_task_number))
            self.answer_edit.setReadOnly(True)
            self.answer_edit.setText(self.current_task_list.get_last_answer(str(self.current_task_number)))
            self.send_btn.hide()
            self.label_tmp_1.show()
            if ans[0]:
                self.label_tmp_1.setText(f"Задание Выполнено(Баллы: {ans[1]})")
                self.label_tmp_1.setStyleSheet("color: green")
            else:
                self.label_tmp_1.setText(f"Неправильный Ответ(Правильный ответ: {ans[2]})")
                self.label_tmp_1.setStyleSheet("color: red")
        self.lcdNumber.display(self.current_task_list.get_score())

    def update_lists(self, index):
        if index == 1:
            self.self_tl.clear()
            #self.self_ut.clear()
            self.form_self_task_lists()
            #self.form_user_task_list()
        if index == 3:
            self.task_history.clear()
            self.load_task_history_names()

    def update_lists(self):
        self.task_history.clear()
        self.load_task_history_names()

    def go_to_task_list_creation(self):
        self.form_task_select()
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget.setTabVisible(2, True)
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.setTabEnabled(1, False)
        # self.tabWidget.setTabEnabled(3, False)

    def cancel_pressed(self):
        self.task_select_items = {}
        if self.current_task_list_number != -1:
            self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(1, True)
        # self.tabWidget.setTabEnabled(3, False)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget.setTabVisible(2, False)
        self.tl_name.clear()

    def save_pressed(self):
        tl = {}
        for i in self.task_select_items.keys():
            if self.task_select_items[i][1] != 0:
                tl[self.task_select_items[i][0]] = self.task_select_items[i][1]
        if len(tl.keys()) != 0:
            if self.tl_name.text() != "":
                name = self.tl_name.text() 
            elif self.tl_name.text() == "":
                self.no_name += 1
                name = f"БезИмени{self.no_name}"
            self.create_self_task_list(name, tasks=tl)
            self.cancel_pressed()
        else:
            imsgBox = QtWidgets.QMessageBox()
            imsgBox.setIcon(QtWidgets.QMessageBox.Information)
            imsgBox.setText("Вы не выбрали ни одного задания!")
            imsgBox.setWindowTitle("Уведомление")
            imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            returnValue = imsgBox.exec()

    def save_current(self, item):
        self.current_item = item

    def add_item(self): 
        self.task_select_items[self.task_select.currentItem().text().split(".")[0]][1] += 1
        self.task_select.currentItem().setText(f"{' '.join(self.task_select.currentItem().text().split()[:-1])}  {self.task_select_items[self.task_select.currentItem().text().split('.')[0]][1]}")
            
    def remove_item(self):
        print(3)
        self.task_select_items[self.task_select.currentItem().text().split(".")[0]][1] -= 1
        self.task_select.currentItem().setText(f"{' '.join(self.task_select.currentItem().text().split()[:-1])}  {self.task_select_items[self.task_select.currentItem().text().split('.')[0]][1]}")

    def on_self_task_list_choice(self, item):
        index = int(item.text().split(".")[0]) - 1
        if self.self_task_lists[index].is_completed():
            imsgBox = QtWidgets.QMessageBox()
            imsgBox.setIcon(QtWidgets.QMessageBox.Information)
            imsgBox.setText("Эта работа уже сдана.")
            imsgBox.setWindowTitle("Уведомление")
            imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            returnValue = imsgBox.exec()
        elif self.current_task_list_number == index:
            imsgBox = QtWidgets.QMessageBox()
            imsgBox.setIcon(QtWidgets.QMessageBox.Information)
            imsgBox.setText("Эта работа выполняется в данное время.")
            imsgBox.setWindowTitle("Уведомление")
            imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            returnValue = imsgBox.exec()
        elif self.current_task_list_number != -1:
            qmsgBox = QtWidgets.QMessageBox()
            qmsgBox.setIcon(QtWidgets.QMessageBox.Question)
            qmsgBox.setText("Вы уверены что хотите начать другую работу?\nВаша текщая работа будет сдана!")
            qmsgBox.setWindowTitle("Подтверждение")
            qmsgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            returnValue = qmsgBox.exec()
            if returnValue == QtWidgets.QMessageBox.Yes:
                imsgBox = QtWidgets.QMessageBox()
                imsgBox.setIcon(QtWidgets.QMessageBox.Information)
                imsgBox.setText(f"Всего заданий: {self.current_task_list.get_amount_of_tasks()}\nЗаданий выполнено правильно: {self.current_task_list.get_amount_of_completed()}\nОбщий балл: {self.current_task_list.get_score()}")
                imsgBox.setWindowTitle("Работа сдана")
                imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                returnValue1 = imsgBox.exec()
                if returnValue1 == QtWidgets.QMessageBox.Ok:
                    self.clear_all()
                    self.choose_task_list(index, is_self=True)
        else:
            qmsgBox = QtWidgets.QMessageBox()
            qmsgBox.setIcon(QtWidgets.QMessageBox.Question)
            qmsgBox.setText("Вы уверены что хотите начать эту работу?")
            qmsgBox.setWindowTitle("Подтверждение")
            qmsgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            returnValue = qmsgBox.exec()
            if returnValue == QtWidgets.QMessageBox.Yes:
                self.choose_task_list(index, is_self=True)
    
    def choose_task(self):
        number = self.task_choose.currentIndex()
        self.current_task_list.save_last_answer(str(self.current_task_number), self.answer_edit.text())
        self.current_task_number = number
        text = self.current_task_list.get_task_by_number(number, get_only_text=True)
        self.task_text.setText(text)
        if not self.current_task_list.is_from_history_check():
            self.check_answer(check_only=True)
        else:
            self.task_solution.setText(self.current_task_list.get_solution(self.current_task_number))
            self.answer_edit.setReadOnly(True)
            self.answer_edit.setText(self.current_task_list.get_user_answer(self.current_task_number))
            #print(self.current_task_list.get_user_answer(self.current_task_number))
            self.label_tmp_1.show()
            is_completed = self.current_task_list.get_task_completeness(self.current_task_number)
            if is_completed:
                self.label_tmp_1.setText(f"Задание Выполнено(Баллы: {self.current_task_list.get_task_score(self.current_task_number)})")
                self.label_tmp_1.setStyleSheet("color: green")
            else:
                self.label_tmp_1.setText(f"Неправильный Ответ(Правильный ответ: {self.current_task_list.get_right_answer(self.current_task_number)})")
                self.label_tmp_1.setStyleSheet("color: red")
            self.label_tmp_1.show()

    def choose_task_list(self, index=-1, is_self=False, is_user=False, is_from_history=False, tl=None):
        if is_self:
            self.current_task_list = self.self_task_lists[index]
        elif is_user:
            self.current_task_list = self.user_task_lists[index]
        elif is_from_history:
            self.current_task_list = tl
        self.current_task_list_number = index
        self.current_task_list.on_run()
        self.form_qcombobox()
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setCurrentIndex(0)
        if is_from_history:
            self.send_btn.hide()
            self.end_work.setText("Завершить просмотр")
            self.current_task_list.update_score()
            self.lcdNumber.display(self.current_task_list.get_score())

    def form_qcombobox(self):
        self.task_choose.clear()
        self.last_field_text = {}
        for i in range(self.current_task_list.get_amount_of_tasks()):
            text = f"{i + 1}. {self.current_task_list.get_task_by_number(i, get_only_name=True)}."
            self.task_choose.addItem(text)
        self.current_task_number = 0
        self.task_choose.setCurrentIndex(self.current_task_number)
        self.choose_task()

    def form_self_task_lists(self):
        c = 1
        for i in self.self_task_lists:
            self.self_tl.addItem(f"{c}. {i.get_name()} ({i.get_status()})")
            c += 1

    def create_task_list(self, name, task_types):
        tl = TaskList(name)
        try:
            tl.form_tasks(task_types)
        except Exception:
            pass
        return tl
            
    def form_task_select(self):
        try:
            self.task_select.clear()
            self.task_select_items = {}
            soc = socket.socket()
            soc.connect(("188.134.74.19", 4444))
            to_send = f"get_name_by_number"
            soc.sendall(to_send.encode())
            data = soc.recv(1024)
            data = data.decode().split("$")
            data = [i.split("|") for i in data]
            soc.close()
            c = 1
            for i in data:
                self.task_select.addItem(f"{c}. {i[1]}. Количество: {0}")
                self.task_select_items[str(c)] = [i[0], 0]
                c += 1
        except Exception:
            imsgBox = QtWidgets.QMessageBox()
            imsgBox.setIcon(QtWidgets.QMessageBox.Information)
            imsgBox.setText("Произошла непредвиденная ошибка.")
            imsgBox.setWindowTitle("Ошибка!")
            imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            imsgBox.exec()

    def save_task_on_server(self):
        data = self.current_task_list.get_all_save_data()
        print(data)
        soc = socket.socket()
        soc.connect(("188.134.74.19", 4444))
        soc.sendall(f"save_data||{self.user_id}||{data}".encode())
        soc.close()

    def load_task_history_names(self):
        soc = socket.socket()
        soc.connect(("188.134.74.19", 4444))
        soc.sendall(f"get_saved_tl_names {self.user_id}".encode())
        dt = soc.recv(1024)
        dt = dt.decode()
        soc.close()
        if dt != "NothingFound":
            dt = dt.split("&")
            for i in dt:
                name, add_info , date = i.split("|")
                self.task_history.addItem(f"{name}({add_info}) {date}")
    
    def load_task_from_history(self, item):
        tl = TaskList("")
        soc = socket.socket()
        tx = self.task_history.row(item)
        soc.connect(("188.134.74.19", 4444))
        soc.sendall(f"get_saved_tl_data|{self.user_id}&{tx}".encode())
        dt = soc.recv(1024)
        dt = dt.decode()
        soc.close()
        dt = dt.split("|")
        sl = {}
        for i in dt:
            dti = i.split(";")
            tid = dti[0]
            dti = dti[1:]
            sp = []
            for j in dti:
                sp.append([*j.split(":")])
            sl[tid] = sp
        print(sl)
        self.clear_all()
        #try:
        tl.load_tasks(sl)
        self.choose_task_list(is_from_history=True, tl=tl)
        #except Exception:
            #pass
        return tl

    def end_task(self):
        qmsgBox = QtWidgets.QMessageBox()
        qmsgBox.setIcon(QtWidgets.QMessageBox.Question)
        if not self.current_task_list.is_from_history_check():
            qmsgBox.setText("Вы уверены что хотите сдать работу?")
        else:
            qmsgBox.setText("Вы уверены что хотите завершить просмотр задания?")
        qmsgBox.setWindowTitle("Подтверждение")
        qmsgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        returnValue = qmsgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Yes:
            imsgBox = QtWidgets.QMessageBox()
            imsgBox.setIcon(QtWidgets.QMessageBox.Information)
            if not self.current_task_list.is_from_history_check():
                imsgBox.setText(f"Всего заданий: {self.current_task_list.get_amount_of_tasks()}\nЗаданий выполнено правильно: {self.current_task_list.get_amount_of_completed()}\nОбщий балл: {self.current_task_list.get_score()}")
                imsgBox.setWindowTitle("Работа сдана")
            else:
                imsgBox.setText("Просмотр задания был завершен.")
                imsgBox.setWindowTitle("Просмотр завершен")
            imsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            returnValue = imsgBox.exec()
            self.clear_all()

    def clear_all(self):
        self.task_choose.clear()
        self.task_text.clear()
        self.label_tmp_1.clear()
        self.answer_edit.setReadOnly(True)
        self.answer_edit.clear()
        self.send_btn.hide()
        self.label_tmp_1.hide()
        if self.current_task_list_number != -1:
            self.current_task_list.on_complete()
            self.save_task_on_server()
            if self.current_task_list.get_type() == "self":
                del self.self_task_lists[self.current_task_list_number]
            elif self.current_task_list.get_type() == "user":
                del self.user_task_lists[self.current_task_list_number]
        self.current_task_list = None
        self.current_task_number = -1
        self.current_task_list_number = -1
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget.setTabEnabled(0, False)
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Program()
    window.show()
    app.exec_()

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text)
  
sys.excepthook = log_uncaught_exceptions

if __name__ == "__main__":
    main()
