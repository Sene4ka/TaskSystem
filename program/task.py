from random import choice
from ftplib import FTP
import os
import socket


class Task:
    def __init__(self, task_id, name, text, max_ball, seed, data, answer):
        self.task_id = task_id
        self.seed = seed
        self.task_name = name
        self.data = data
        self.task_text = text.format(*data)
        self.answer = answer
        self.score = "0"
        self.max_ball = max_ball
        self.completed = False
        self.first_try = True


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

        
        
        

        
