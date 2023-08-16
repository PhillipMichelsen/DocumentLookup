import json


class ResponseHold:
    def __init__(self):
        self.response_hold = {}

    def stash_job_data(self, task_id, job_data):
        self.response_hold[task_id] = job_data

    def get_job_data(self, task_id):
        return self.response_hold[task_id]

    def clear_job_data(self, task_id):
        self.response_hold.pop(task_id)


response_hold = ResponseHold()
