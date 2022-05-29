class Context:
    """Object to store all users data in a conversation"""

    def __init__(self) -> None:
        self.users_data = {}

    def add_user(self, phone_num):
        self.users_data[str(phone_num)] = {}

    def user_exists(self, phone_num):
        if len(self.users_data):
            if phone_num in self.users_data.keys():
                return True


context = Context()


class user_context():
    """Object that manages a specific user's data in a conversation.
    The user's phone number is used as the id"""

    def __init__(self, phone_num) -> None:
        if not context.user_exists(phone_num):
            context.add_user(phone_num)
        self.user_data = context.users_data[str(phone_num)]
