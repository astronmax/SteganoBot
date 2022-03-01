class User:
    id = None
    state = 0
    active_attachment = None

    def __init__(self, vk_id):
        self.id = vk_id
        print("New User with id: " + str(self.id))

    def __getattr__(self, item):
        return self.item

    def __str__(self):
        return "User id: {}, state: {}, active_attachment: {}"\
            .format(self.id, self.state, self.active_attachment)
