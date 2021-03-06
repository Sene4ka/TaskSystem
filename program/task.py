from random import choice
from ftplib import FTP


class Task:
    def __init__(self, task_id, name, task_text, solution_text, max_ball, seed, text_data, solution_data, answer):
        self.task_id = task_id
        self.seed = seed
        self.task_name = name
        self.text_data = text_data
        self.task_text = task_text.format(*self.text_data)
        self.solution_data = solution_data
        self.task_solution = solution_text.format(*self.solution_data)
        self.answer = answer
        self.score = "0"
        self.max_ball = max_ball
        self.completed = False
        self.first_try = True
        self.user_answer = None

    def set_preferred_parameters(self, user_answer):
        self.user_answer = user_answer
        self.first_try = False
        self.completed = True if self.answer == self.user_answer else False
        self.score = self.max_ball if self.answer == self.user_answer else self.score

    def get_task_id(self):
        return self.task_id

    def get_seed(self):
        return self.seed
    
    def get_max_ball(self):
        return self.max_ball

    def get_score(self):
        return self.score

    def get_text(self):
        return self.task_text
    
    def get_answer(self):
        return self.answer

    def get_user_answer(self):
        return self.user_answer

    def get_name(self):
        return self.task_name

    def is_completed(self):
        return self.completed

    def get_solution(self):
        return self.task_solution

    def get_all_save_data(self):
        return f"{self.task_id};{self.seed};{self.user_answer}"

    def on_task_complete(self, answer=None, check_only=False):
        if check_only:
            return self.completed, self.score, self.answer, self.first_try, False
        elif self.first_try:
            self.first_try = False
            if answer == self.answer:
                self.score = self.max_ball
                self.completed = True
            self.user_answer = answer
            return self.completed, self.score, self.answer, self.first_try, True
        else:
            return self.completed, self.score, self.answer, self.first_try, False

        
        
        

        
