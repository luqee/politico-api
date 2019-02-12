class  Office(object):
    def __init__(self, office_data):
        self.name = office_data['name']
        self.type = office_data['office_type']
        self.description = office_data['description']