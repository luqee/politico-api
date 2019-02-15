import datetime
from app.api.v1 import models

class Politico(object):
    def __init__(self):
        self.registered_users = []
        self.registered_parties = []
        self.registered_offices = []

    def get_parties(self):
        return self.registered_parties

    def get_offices(self):
        return self.registered_offices
    
    def get_user_by_id(self, user_id):
        for user in self.registered_users:
            if user.id == int(user_id):
                return user
        return 'Not found'

    def get_user(self, email):
        for user in self.registered_users:
            if user.email == email:
                return user
        return 'Not found'

    def get_resource_by_id(self, resource_id, resource_type):
        if resource_type == 'party':
            for party in self.registered_parties:
                if party.id == resource_id:
                    return party
            return 'Not found'  
        elif resource_type == 'office':
            for office in self.registered_offices:
                if office.id == resource_id:
                    return office
            return 'Not found'

    def register_user(self, user_data):
        # check if user exists
        if self.get_user(user_data['email']) == 'Not found':
            # check if othername is taken
            othernames = [user.othername for user in self.registered_users]
            if user_data['othername'] in othernames:
                return 'Other name taken'
            # Add user as they don't exist
            if user_data['is_admin']:
                new_user = models.user.Admin(
                    firstname=user_data['firstname'],
                    lastname=user_data['lastname'],
                    email=user_data['email'],
                    othername=user_data['othername'],
                    phone_number=user_data['phone_number'],
                    address=user_data.get('address'),
                    is_admin=user_data['is_admin'],
                    is_politician=user_data['is_politician'],
                    password=user_data['password']
                )
            elif user_data['is_politician']:
                new_user = models.user.Politician(
                    firstname=user_data['firstname'],
                    lastname=user_data['lastname'],
                    email=user_data['email'],
                    othername=user_data['othername'],
                    phone_number=user_data['phone_number'],
                    home_county=user_data.get('home_county'),
                    is_admin=user_data['is_admin'],
                    is_politician=user_data['is_politician'],
                    password=user_data['password']
                )
            else:
                new_user = models.user.User(
                    firstname=user_data['firstname'],
                    lastname=user_data['lastname'],
                    email=user_data['email'],
                    othername=user_data['othername'],
                    phone_number=user_data['phone_number'],
                    is_admin=user_data['is_admin'],
                    is_politician=user_data['is_politician'],
                    password=user_data['password']
                )
            new_user.id = len(self.registered_users) + 1
            
            self.registered_users.append(new_user)
            return 'User added'
        else:
            return 'User already exists'
    
    def login_user(self, user_data):
        user = self.get_user(user_data['email'])
        if user == 'Not found':
            return 'Invalid credentials'
        elif isinstance(user, models.user.User):
            if user.verify_password(user_data['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token()
                return access_token
            else:
                return 'Invalid credentials'

    def check_resource_exists(self, resource_type, resource):
        if resource_type == 'party':
            # check if it exists
            for party in self.registered_parties:
                if party.name == resource['name']:
                    return True
            return False
        elif resource_type == 'office':
            for office in self.registered_offices:
                if office.name == resource['name']:
                    return True
            return False

    def create_resource(self, current_user, resource, resource_type):
        if current_user.is_admin:
            if self.check_resource_exists(resource_type, resource):
                return '{} exists'.format(resource_type.capitalize())
            else:
                if resource_type == 'party':
                    new_party = models.party.Party(resource)
                    new_party.id = len(self.registered_parties) + 1
                    self.registered_parties.append(new_party)
                    return new_party
                elif resource_type == 'office':
                    new_office = models.office.Office(resource)
                    new_office.id = len(self.registered_offices) + 1
                    self.registered_offices.append(new_office)
                    return new_office
        return 'Forbiden'
    
    def update_resource(self, resource_type, resource_id, resource):
        if resource_type == 'party':
            party = self.get_resource_by_id(resource_id, resource_type)
            if party == 'Not found':
                return 'Party not found'
            elif type(party) == models.party.Party:
                party.name = resource['name']
                party.hq_address = resource['hq_address']
                party.logo_url = resource['logo_url']
                party.description = resource['description']
                return party
        elif resource_type == 'office':
            office = self.get_resource_by_id(resource_id, resource_type)
            if office == 'Not found':
                return 'Office not found'
            office.name = resource['name']
            office.type = resource['office_type']
            office.description = resource['description']
            return office
    
    def delete_resource(self, resource_type, resource_id):
        if resource_type == 'party':
            party = self.get_resource_by_id(resource_id, resource_type)
            if party == 'Not found':
                return 'Party not found'
            elif type(party) == models.party.Party:
                self.registered_parties.remove(party)
                return 'Party deleted'
        elif resource_type == 'office':
            office = self.get_resource_by_id(resource_id, resource_type)
            if office == 'Not found':
                return 'Office not found'
            elif type(office) == models.office.Office:
                self.registered_offices.remove(office)
                return 'Office deleted'
