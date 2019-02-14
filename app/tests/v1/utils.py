import datetime

class Utils(object):
    def __init__(self):
        pass
    ADMIN = {
        'firstname': 'Luda',
        'lastname': 'one',
        'othername': 'politic',
        'email': 'politician@app.com',
        'phone_number': '254726094972',
        'passportUrl' : 'some/url/pass.jpg',
        'address': '123 fith street',
        'password': 'password',
        'is_admin': 'True',
        'is_politician': 'False'
    }
    POLITICIAN = {
        'firstname': 'Donald',
        'lastname': 'Duck',
        'othername': 'quack',
        'email': 'admin@app.com',
        'phone_number': '254726094972',
        'passportUrl' : 'some/url/pass.jpg',
        'home_county': 'Rongai',
        'password': 'password',
        'is_admin': 'False',
        'is_politician': 'True'
    }

    USER = {
        'firstname': 'Luda',
        'lastname': 'one',
        'othername': 'luqee',
        'email': 'user@app.com',
        'phone_number': '254726094972',
        'passportUrl' : 'some/url/pass.jpg',
        'password': 'password',
        'is_admin': 'False',
        'is_politician': 'False'
    }

    PARTIES = [
        {
            'name': 'Chama Kikuu',
            'hq_address': '564 Lon Road',
            'logo_url': 'url/to/logo.jpg',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
        },
        {
            'name': 'Party 2',
            'hq_address': '786 city square',
            'logo_url': 'url/to/logo.jpg',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
        },
    ]
    OFFICES = [
        {
            'name': 'President',
            'office_type': 'State',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
        },
        {
            'name': 'Women Rep',
            'office_type': 'Legislative',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
        },
        {
            'name': 'Chief',
            'office_type': 'Local Government',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitatio'
        },
    ]
    def register_user(self, client, user_type):
        if user_type == 'admin':
            client.post('api/v1/auth/user/register', json=self.ADMIN)
        elif user_type == 'politician':
            client.post('api/v1/auth/user/register', json=self.POLITICIAN)
        else:
            client.post('api/v1/auth/user/register', json=self.USER)

    def login_user(self, client, user_type):
        
        if user_type == 'admin':
            data = {
                'email': self.ADMIN['email'],
                'password': self.ADMIN['password']
            }
            return client.post('api/v1/auth/user/login', json=data)
        elif user_type == 'politician':
            data = {
                'email': self.POLITICIAN['email'],
                'password': self.POLITICIAN['password'],
            }
            return client.post('api/v1/auth/user/login', json=data)
        else:
            data = {
                'email': self.USER['email'],
                'password': self.USER['password'],
            }
            return client.post('api/v1/auth/user/login', json=data)

    def create_party(self, client, party, headers):
        client.post('api/v1/parties', json=party, headers=headers)
    
    def create_office(self, client, office, headers):
        client.post('api/v1/offices', json=office, headers=headers)
    
    def create_parties(self, client, headers):
        for party in self.PARTIES:
            client.post('api/v1/parties', json=party, headers=headers)
    
    def create_offices(self, client, headers):
        for office in self.OFFICES:
            client.post('api/v1/offices', json=office, headers=headers)
