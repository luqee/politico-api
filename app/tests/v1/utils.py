import datetime

class Utils(object):
    def __init__(self):
        pass
    ADMIN = {
        'firstname': 'Luda',
        'lastname': 'one',
        'othername': 'quack',
        'email': 'politician@app.com',
        'phone_number': '+254726094972',
        'passportUrl' : 'some/url/pass.jpg',
        'address': '123 fith street',
        'password': 'password',
        'user_type': 'admin'
    }
    POLITICIAN = {
        'firstname': 'Donald',
        'lastname': 'Duck',
        'othername': 'quack',
        'email': 'admin@app.com',
        'phone_number': '+254726094972',
        'passportUrl' : 'some/url/pass.jpg',
        'home_county': 'Rongai',
        'password': 'password',
        'user_type': 'politician'
    }

    USER = {
        'firstname': 'Luda',
        'lastname': 'one',
        'othername': 'quack',
        'email': 'user@app.com',
        'phone_number': '+254726094972',
        'passportUrl' : 'some/url/pass.jpg',
        'password': 'password',
        'user_type': 'user'
    }

    def register_user(self, client, user_type):
        if user_type == 'admin':
            client.post('api/v1/auth/user/register', json=self.ADMIN)
        elif user_type == 'politician':
            client.post('api/v1/auth/user/register', json=self.POLITICIAN)
        else:
            client.post('api/v1/auth/user/register', json=self.USER)
