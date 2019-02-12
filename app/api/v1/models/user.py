from flask import current_app as app
from datetime import datetime, timedelta
import jwt
import bcrypt

class User(object):
    def __init__(self, kwargs):
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.phoneNumber = kwargs.get('phone_number')
        self.password = bcrypt.hashpw(kwargs.get('password').encode('utf8'), bcrypt.gensalt())
        self.is_admin = kwargs.get('is_admin')
        self.is_politician = kwargs.get('is_politician')

    def verify_password(self, password):
        if bcrypt.checkpw(password.encode('utf8') , self.password):
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

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

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
    def __init__(self, kwargs):
        self.address = kwargs.get('address')
        super(Admin, self).__init__(kwargs)

class Politician(User):
    def __init__(self, kwargs):
        self.home_county = kwargs.get('home_county')
        super(Politician, self).__init__(kwargs)
