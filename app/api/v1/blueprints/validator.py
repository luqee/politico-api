import re
from flask import abort
class Validator(object):
    def __init__():
        pass

    @staticmethod
    def validate_user(user_object):
        for key, value in user_object.items():
            # ensure keys have values
            if not value:
                abort(422, "{} is lacking. It is a required field".format(key))
            if key == 'email':
                if Validator.check_email(value) == 'Invalid email':
                    abort(422, '{} is invalid'.format(key))
            if key == 'phone_number':
                if Validator.check_number(value) == 'Invalid number':
                    abort(422, '{} is invalid'.format(key))
            # validate length
            if key == "username" or key == "firstname" or key == "lastname" or key == "username":
                if len(value) < 3:
                    abort(422, "The {} provided is too short".format(key))
                elif len(value) > 15:
                    abort(422, "The {} provided is too long".format(key))
        return True
    
    @staticmethod
    def check_email(email):
        email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        match_object = re.match(email_pattern, email)
        if match_object is None:
            return 'Invalid email'
        return 'Valid email'
    
    @staticmethod
    def check_number(number):
        number_pattern = re.compile('(^\d{3}\d{3}\d{6}$)')
        match_object = re.match(number_pattern, number)
        if match_object is None:
            return 'Invalid number'
        return 'Valid number'