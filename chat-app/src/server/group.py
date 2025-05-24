class GroupChat:
    def __init__(self):
        self.groups = {}

    def create_group(self, group_name):
        if group_name not in self.groups:
            self.groups[group_name] = []
            return f"Group '{group_name}' created successfully."
        else:
            return f"Group '{group_name}' already exists."

    def add_user_to_group(self, group_name, user):
        if group_name in self.groups:
            if user not in self.groups[group_name]:
                self.groups[group_name].append(user)
                return f"User '{user}' added to group '{group_name}'."
            else:
                return f"User '{user}' is already in group '{group_name}'."
        else:
            return f"Group '{group_name}' does not exist."

    def remove_user_from_group(self, group_name, user):
        if group_name in self.groups:
            if user in self.groups[group_name]:
                self.groups[group_name].remove(user)
                return f"User '{user}' removed from group '{group_name}'."
            else:
                return f"User '{user}' is not in group '{group_name}'."
        else:
            return f"Group '{group_name}' does not exist."

    def get_group_users(self, group_name):
        if group_name in self.groups:
            return self.groups[group_name]
        else:
            return f"Group '{group_name}' does not exist."