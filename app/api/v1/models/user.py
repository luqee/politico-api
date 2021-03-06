from datetime import datetime, timedelta
from flask import current_app as app
import jwt
import bcrypt

class User(object):
    '''Class representing the base user '''
    def __init__(self, **kwargs):
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('othername')
        self.email = kwargs.get('email')
        self.phone_number = kwargs.get('phone_number')
        self.password = bcrypt.hashpw(kwargs.get('password').encode('utf8'), bcrypt.gensalt())
        self.is_admin = kwargs.get('is_admin')
        self.is_politician = kwargs.get('is_politician')

    def verify_password(self, password):
        ''' Function to verify password'''
        if bcrypt.checkpw(password.encode('utf8'), self.password):
            return True
        return False

    def generate_token(self):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=45),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as exception:
            # return an error in string format if an exception occurs
            return str(exception)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

class Admin(User):
    '''Class representing a admin '''
    def __init__(self, **kwargs):
        self.address = kwargs.get('address')
        super(Admin, self).__init__(**kwargs)

class Politician(User):
    '''Class representing a politician '''
    def __init__(self, **kwargs):
        self.home_county = kwargs.get('home_county')
        super(Politician, self).__init__(**kwargs)
