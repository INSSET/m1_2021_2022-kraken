class Group:
    def __init__(self, group_id, group_name, users_names):
        self.group_id = group_id
        self.group_name = group_name
        self.users_names = list(users_names)
