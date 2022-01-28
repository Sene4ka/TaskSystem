from random import choice
from ftplib import FTP


class Task:
    def __init__(self, task_id, name, task_text, solution_text, max_ball, seed, text_data, solution_data, answer):
        self.task_id = task_id
        self.seed = seed
        self.task_name = name
        print("IN_CLASS")
        self.text_data = text_data
        print("IN_CLASS")
        self.task_text = task_text.format(*self.text_data)
        print("IN_CLASS")
        self.solution_data = solution_data
        print("IN_CLASS", solution_text, '\n', solution_data)
        self.task_solution = solution_text.format(*self.solution_data)
        print("IN_CLASS")
        self.answer = answer
        print("IN_CLASS")
        self.score = "0"
        self.max_ball = max_ball
        self.completed = False
        self.first_try = True
        print("IN_CLASS:", self.task_text, self.task_solution)


    def get_task_id(self):
        return self.task_id

    def get_seed(self):
        return self.seed

    def get_text(self):
        return self.task_text
    
    def get_answer(self):
        return self.answer

    def get_name(self):
        return self.task_name

    def is_completed(self):
        return self.completed

    def get_solution(self):
        return self.task_solution

    def on_task_complete(self, answer=None, check_only=False):
        if check_only:
            return self.completed, self.score, self.answer, self.first_try, False
        elif self.first_try:
            self.first_try = False
            if answer == self.answer:
                self.score = self.max_ball
                self.completed = True
            return self.completed, self.score, self.answer, self.first_try, True
        else:
            return self.completed, self.score, self.answer, self.first_try, False

        
        
        

        
