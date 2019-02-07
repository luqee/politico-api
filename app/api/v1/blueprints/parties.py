from flask import Blueprint, request, jsonify, g
from app.api.v1.models import party
from app import politico
from .decorators import login_required

party_blueprint = Blueprint('parties', __name__, url_prefix='/api/v1')

@party_blueprint.route('/parties', methods=['POST'])
@login_required
def create_party():
    data = request.get_json()
    name = data['name']
    hq_address = data['hq_address']
    logo_url = data['logo_url']
    description = data['description']
    
    new_party = party.Party(name=name, hq_address=hq_address, logo_url=logo_url, description=description)
    result = politico.create_party(g.user, new_party)
    if result == 'Party created':
        response = {
            'status': 201,
            'data':[{'message': 'Party created successfully.'}]
        }
        return jsonify(response), 201
    elif result == 'Login needed':
        response = {
            'status': 400,
            'error': 'You need to login before creating a party'
        }
        return jsonify(response), 400