class Party(object):
    def __init__(self, party_data):
        self.name = party_data['name']
        self.hq_address = party_data['hq_address']
        self.logo_url = party_data['logo_url']
        self.description = party_data['description']
