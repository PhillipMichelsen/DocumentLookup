class ResponseHold:
    def __init__(self):
        self.response_hold = {}

    def stash_response(self, task_id, response):
        self.response_hold[task_id] = response

    def get_response(self, task_id):
        return self.response_hold[task_id]

    def clear_response(self, task_id):
        self.response_hold.pop(task_id)


response_hold = ResponseHold()
