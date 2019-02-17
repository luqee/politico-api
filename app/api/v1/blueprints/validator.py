import re

class Validator(object):
    ''' Validator class '''

    @staticmethod
    def validate_user(user_object):
        ''' Validates the user '''
        response = {}
        for key, value in user_object.items():
            if key in ('is_admin', 'is_politician'):
                if not isinstance(value, bool):
                    response['status'] = 400
                    response['error'] = '{} needs to be boolean'.format(key)
                    break
            # ensure keys have values
            else:
                if not value:
                    response['status'] = 400
                    response['error'] = 'Please provide your {}'.format(key)
                    break
                if not value.strip():
                    response['status'] = 400
                    response['error'] = '{} is invalid'.format(key)
                    break
                if key == 'email':
                    if Validator.check_email(value) == 'Invalid email':
                        response['status'] = 400
                        response['error'] = '{} is invalid'.format(key)
                        break
                if key == 'phone_number':
                    if Validator.check_number(value) == 'Invalid number':
                        response['status'] = 400
                        response['error'] = '{} is invalid'.format(key)
                        break
                # validate length
                if key in ('firstname', 'lastname', 'othername'):
                    if len(value) < 3:
                        response['status'] = 400
                        response['error'] = 'The {} provided is too short'.format(key)
                        break
                    elif len(value) > 15:
                        response['status'] = 400
                        response['error'] = 'The {} provided is too long'.format(key)
                        break
        if response:
            return response
        return True

    @staticmethod
    def validate_party(party_object):
        ''' Validate a party '''
        response = {}
        for key, value in party_object.items():
            # ensure keys have values
            if not value:
                response['status'] = 400
                response['error'] = 'Please provide the {}'.format(key)
                break
            if not value.strip():
                response['status'] = 400
                response['error'] = 'Please provide a valid {}'.format(key)
                break
            # validate length
            if key in ('name', 'hq_address'):
                if len(value) < 3:
                    response['status'] = 400
                    response['error'] = 'The {} provided is too short'.format(key)
                    break
                elif len(value) > 15:
                    response['status'] = 400
                    response['error'] = 'The {} provided is too long'.format(key)
                    break
        if response:
            return response
        return True

    @staticmethod
    def validate_office(office_object):
        ''' Validate an office '''
        response = {}
        office_types = ['federal', 'legislative', 'state', 'local government']
        for key, value in office_object.items():
            # ensure keys have values
            if not value:
                response['status'] = 400
                response['error'] = 'Please provide the {}'.format(key)
                break
            if not value.strip():
                response['status'] = 400
                response['error'] = 'Please provide a valid {}'.format(key)
                break
            # validate length
            if key == "name":
                if len(value) < 3:
                    response['status'] = 400
                    response['error'] = 'The {} provided is too short'.format(key)
                    break
                elif len(value) > 15:
                    response['status'] = 400
                    response['error'] = "The {} provided is too long".format(key)
                    break
            if key == 'office_type':
                if value.lower() not in office_types:
                    response['status'] = 400
                    response['error'] = "The {} provided is invalid".format(key)
                    break
        if response:
            return response
        return True

    @staticmethod
    def check_email(email):
        ''' Email validator '''
        email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        match_object = re.match(email_pattern, email)
        if match_object is None:
            return 'Invalid email'
        return 'Valid email'

    @staticmethod
    def check_number(number):
        ''' Phone number validator '''
        number_pattern = re.compile(r'(^\d{3}\d{3}\d{6}$)')
        match_object = re.match(number_pattern, number)
        if match_object is None:
            return 'Invalid number'
        return 'Valid number'
