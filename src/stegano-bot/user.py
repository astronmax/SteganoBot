class User:
    """
    This class saves user's ids and states
    """
    id = None
    state = 0

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

        :return: Id, State
        """
        return "User id: {}, state: {}"\
            .format(self.id, self.state)
