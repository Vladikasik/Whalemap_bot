import json


class DB:

    def __init__(self):

        self.groups_file = "groups.json"
        self.users_file = "users.json"

    def write_data(self, data, group=False, user=False):
        if group:
            with open(self.groups_file, "r") as file:
                groups_data = json.load(file)
            if data[0] not in groups_data[data[1]][data[2]]:
                groups_data[data[1]][data[2]].append(data[0])
                with open(self.groups_file, 'w') as file:
                    json.dump(groups_data, file, indent=4)
                print('groups updated')
            else:
                print('user already subsribed to this plan')

        elif user:
            with open(self.users_file, "r") as file:
                users_data = json.load(file)
            data[0] = str(data[0])
            try:
                if str(data[1]) not in users_data[data[0]]:
                    users_data[data[0]].append(data[1])
                else:
                    print('user already exists')
            except KeyError:
                users_data[int(data[0])] = [data[1]]
            with open(self.users_file, 'w') as file:
                json.dump(users_data, file)
            print('users updated')

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
