from flask import current_app as app

class User(object):
    def __init__(self, kwargs):
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.phoneNumber = kwargs.get('phone_number')
        self.password = kwargs.get('password')
        self.user_type = kwargs.get('user_type')

class Admin(User):
    def __init__(self, kwargs):
        self.address = kwargs.get('address')
        super(Admin, self).__init__(kwargs)

class Politician(User):
    def __init__(self, kwargs):
        self.home_county = kwargs.get('home_county')
        super(Politician, self).__init__(kwargs)