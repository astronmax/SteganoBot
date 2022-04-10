class User:
    """
    This class saves user's ids, states and last attachment
    """
    id = None
    state = 0
    active_attachment = None

    def __init__(self, vk_id):
        """
        Saves user's id

        :param vk_id: User's vk id
        """
        self.id = vk_id
        print("New User with id: " + str(self.id))

    def __str__(self):
        """
        Converts user into a printable string

        :return: Id, State, Attachment
        """
        return "User id: {}, state: {}, active_attachment: {}"\
            .format(self.id, self.state, self.active_attachment)
