import pickle

users_info = {}


async def load_users():
    """
    Loads users from 'users.pickle' file
    :return: dictionary {id:User}
    """
    with open("users.pickle", "rb") as file:
        users_info_loaded = pickle.load(file)
    print("Users loaded")
    return users_info_loaded


async def save_users(data):
    """
    Saves users to 'users.pickle' file
    :return: None
    """
    with open("users.pickle", "wb") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("Users saved")
