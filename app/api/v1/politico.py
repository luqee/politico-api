import datetime
from app.api.v1 import models

class Politico(object):
    def __init__(self):
        self.registered_users = []
    
    def get_user(self, email):
        for user in self.registered_users:
            if user.email == email:
                return user
        return 'Not found'

    def register_user(self, user_data):
        # check if user exists
        print(user_data)
        if self.get_user(user_data['email']) == 'Not found':
            # Add user as they don't exist
            if user_data['user_type'] == 'admin':
                new_user = models.user.Admin(user_data)
            elif user_data['user_type'] == 'politician':
                new_user = models.user.Politician(user_data)
            else:
                new_user = models.user.User(user_data)
            new_user.id = len(self.registered_users) + 1
            
            self.registered_users.append(new_user)
            return 'User added'
        else:
            return "User already exists"
