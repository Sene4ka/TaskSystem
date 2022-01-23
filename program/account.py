class Account:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_task_lists = {}

    def get_user_id(self):
        return self.user_id
    
    def get_user_tasks(self):
        return self.user_task_lists
    
    def load_user_tasks(self):
        # sql connect
        pass