from flask import Blueprint, request, jsonify, g
from app.api.v1.models.party import Party
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
    
    new_party = Party(name=name, hq_address=hq_address, logo_url=logo_url, description=description)
    result = politico.create_party(g.user, new_party)
    if type(result) == Party:
        response = {
            'status': 201,
            'data':[{
                'id': result.id,
                'name': result.name
            }]
        }
        return jsonify(response), 201
    elif result == 'Not authorised':
        response = {
            'status': 401,
            'error': 'You need to login before creating a party'
        }
        return jsonify(response), 401

@party_blueprint.route('/parties/<int:party_id>', methods=['GET'])
def get_party(party_id):
    party = politico.get_party_by_id(party_id)
    if party == 'Not found':
        response = {
            'status': 404,
            'error': 'Party not found'
        }        
        return jsonify(response), 404
    if type(party) == Party:
        response = {
            'status': 200,
            'data':[]
        }
        response['data'].append({
            'id': party.id,
            'name': party.name,
            'logo_url': party.logo_url
        })
        return jsonify(response), 200