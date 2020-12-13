import json


class DB:

    def __init__(self):

        self.groups_file = "groups.json"
        self.users_file = "users.json"

    def write_user(self, data, group=False, user=False):
        if group:
            with open(self.groups_file, "r") as file:
                groups_data = json.load(file)
            groups_data[data[1]][data[2]].append(data[0])
            with open(self.groups_file, 'w') as file:
                json.dump(groups_data, file, indent=4)
            print('groups updated')
        elif user:
            with open(self.users_file, "r") as file:
                users_data = json.load(file)
            users_data[data[0]] = data[1]

    def get_user(self, user_id):
        with open(self.users_file, "r") as file:
            users_data = json.load(file)
        to_return = users_data[user_id]
        return to_return

    def get_group(self, group, plan):
        with open(self.groups_file, "r") as file:
            groups_data = json.load(file)
        to_return = groups_data[group][plan]
        return to_return
