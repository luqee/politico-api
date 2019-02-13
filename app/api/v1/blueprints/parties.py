from flask import Blueprint, request, jsonify, g
from app.api.v1.models.party import Party
from app import politico
from .decorators import login_required
from app.api.v1.blueprints.validator import Validator

party_blueprint = Blueprint('parties', __name__, url_prefix='/api/v1')

@party_blueprint.route('/parties', methods=['POST'])
@login_required
def create_party():
    data = request.get_json()
    if not data:
        response = {
            'status': 400,
            'error': 'Request is empty'
        }
        return jsonify(response), 400
    party_data = {
        'name': data.get('name'),
        'hq_address': data.get('hq_address'),
        'logo_url': data.get('logo_url'),
        'description': data.get('description')
    }
    if Validator.validate_party(party_data):
        result = politico.create_party(g.user, party_data)
        # new_party = Party(name=name, hq_address=hq_address, logo_url=logo_url, description=description)
    if type(result) == Party:
        response = {
            'status': 201,
            'data':[{
                'id': result.id,
                'name': result.name
            }]
        }
        return jsonify(response), 201
    elif result == 'Forbiden':
        response = {
            'status': 403,
            'error': 'You need to be an admin to create a party'
        }
        return jsonify(response), 403
    elif result == 'Party exists':
        response = {
            'status': 409,
            'error': 'Party exists'
        }
        return jsonify(response), 409

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

@party_blueprint.route('/parties', methods=['GET'])
def get_parties():
    parties = politico.get_parties()
    if type(parties) == list:
        response = {
            'status': 200,
            'data':[]
        }
        for party in parties:
            response['data'].append({
                'id': party.id,
                'name': party.name,
                'logo_url': party.logo_url
            })
        return jsonify(response), 200

@party_blueprint.route('/parties/<int:party_id>/name', methods=['PATCH'])
@login_required
def update_party(party_id):
    name = request.get_json()['name']
    party = politico.update_party(party_id, name)
    if type(party) == Party:
        response = {
            'status': 200,
            'data':[]
        }
        response['data'].append({
            'id': party.id,
            'name': party.name
        })
        return jsonify(response), 200
    elif party == 'Party not found':
        response = {
            'status': 404,
            'data':[{
                'error': 'Party not found'
            }]
        }
        return jsonify(response, 404)

@party_blueprint.route('/parties/<int:party_id>', methods=['DELETE'])
@login_required
def delete_party(party_id):
    result = politico.delete_party(party_id)
    if result == 'Party deleted':
        response = {
            'status': 202,
            'data':[]
        }
        response['data'].append({
            'message': 'Party deleted successfully'
        })
        return jsonify(response), 202
    elif party == 'Party not found':
        response = {
            'status': 404,
            'data':[{
                'error': 'Party not found'
            }]
        }
        return jsonify(response, 404)
