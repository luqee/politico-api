import datetime
from app.api.v1 import models

class Politico(object):
    def __init__(self):
        self.registered_users = []
        self.registered_parties = []
        self.registered_offices = []
    
    def get_user(self, email):
        for user in self.registered_users:
            if user.email == email:
                return user
        return 'Not found'
    
    def get_user_by_id(self, user_id):
        for user in self.registered_users:
            if user.id == int(user_id):
                return user
        return 'Not found'

    def get_party_by_id(self, party_id):
        for party in self.registered_parties:
            if party.id == party_id:
                return party
        return 'Not found'

    def get_office_by_id(self, office_id):
        for office in self.registered_offices:
            if office.id == office_id:
                return office
        return 'Not found'

    def register_user(self, user_data):
        # check if user exists
        if self.get_user(user_data['email']) == 'Not found':
            # Add user as they don't exist
            if user_data['is_admin'] == 'True':
                new_user = models.user.Admin(user_data)
            elif user_data['is_politician'] == 'True':
                new_user = models.user.Politician(user_data)
            else:
                new_user = models.user.User(user_data)
            new_user.id = len(self.registered_users) + 1
            
            self.registered_users.append(new_user)
            return 'User added'
        else:
            return "User already exists"
    
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

    def create_party(self, current_user, party_data):
        if current_user.is_admin:
            new_party = models.party.Party(party_data)
            for party in self.registered_parties:
                if party.name == new_party.name:
                    return 'Party exists'
            new_party.id = len(self.registered_parties) + 1
            self.registered_parties.append(new_party)
            return new_party
        return 'Forbiden'
    
    def get_parties(self):
        return self.registered_parties
    
    def update_party(self, party_id, name):
        party = self.get_party_by_id(party_id)
        if party == 'Not found':
            return 'Party not found'
        party.name = name
        return party
    
    def delete_party(self, party_id):
        party = self.get_party_by_id(party_id)
        if party == 'Not found':
            return 'Party not found'
        self.registered_parties.remove(party)
        return 'Party deleted'
    
    def create_office(self, current_user, office_data):
        if current_user.is_admin == 'True':
            new_office = models.office.Office(office_data)
            for office in self.registered_offices:
                if office.name == new_office.name:
                    return 'Office exists'
            new_office.id = len(self.registered_offices) + 1
            self.registered_offices.append(new_office)
            return new_office
        return 'Forbiden'

    def get_offices(self):
        return self.registered_offices
    
    def update_office(self, office_id, name):
        office = self.get_office_by_id(office_id)
        if office == 'Not found':
            return 'Office not found'
        office.name = name
        return office
    
    def delete_office(self, office_id):
        office = self.get_office_by_id(office_id)
        if office == 'Not found':
            return 'Office not found'
        self.registered_offices.remove(office)
        return 'Office deleted'
