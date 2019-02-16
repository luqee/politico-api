from flask import Blueprint, request, make_response, jsonify, g
from app.api.v1.models.party import Party
from app import politico
from app.api.v1.blueprints.decorators import login_required
from app.api.v1.blueprints.validator import Validator

party_blueprint = Blueprint('parties', __name__, url_prefix='/api/v1')

@party_blueprint.route('/parties', methods=['POST'])
@login_required
def create_party():
    ''' Route to create a party '''
    data = None
    response = {
        'status': 400,
        'error': 'Provide name, hq_address, logo_url and description as json.'
    }
    try:
        data = request.get_json()
    except:
        return make_response(jsonify(response), 400)
    if not data:
        return make_response(jsonify(response), 400)

    party_data = {
        'name': data.get('name'),
        'hq_address': data.get('hq_address'),
        'logo_url': data.get('logo_url'),
        'description': data.get('description')
    }
    valdiator_result = Validator.validate_party(party_data)
    if isinstance(valdiator_result, dict):
        return make_response(jsonify(valdiator_result), valdiator_result['status'])
    if isinstance(valdiator_result, bool) and valdiator_result:
        result = politico.create_resource(g.user, party_data, 'party')

    response = {}
    if isinstance(result, Party):
        response['status'] = 201
        response['data'] = []
        response['data'].append({
            'id': result.id,
            'name': result.name
        })
    elif result == 'Forbiden':
        response['status'] = 403
        response['error'] = 'You need to be an admin to create a party'
    elif result == 'Party exists':
        response['status'] = 409
        response['data'] = []
        response = {
            'status': 409,
            'error': 'Party exists'
        }
    return make_response(jsonify(response), response['status'])

@party_blueprint.route('/parties/<int:party_id>', methods=['GET'])
def get_party(party_id):
    ''' Route to get specific party '''
    party = politico.get_resource_by_id(party_id, 'party')
    response = {}
    if party == 'Not found':
        response['status'] = 404
        response['error'] = 'Party not found'
    if isinstance(party, Party):
        response['status'] = 200
        response['data'] = []
        response['data'].append({
            'id': party.id,
            'name': party.name,
            'logo_url': party.logo_url
        })
    return make_response(jsonify(response), response['status'])

@party_blueprint.route('/parties', methods=['GET'])
def get_parties():
    ''' Route to get all parties '''
    parties = politico.get_parties()
    response = {}
    if isinstance(parties, list):
        response['status'] = 200
        response['data'] = []
        for party in parties:
            response['data'].append({
                'id': party.id,
                'name': party.name,
                'logo_url': party.logo_url
            })
    return make_response(jsonify(response), response['status'])

@party_blueprint.route('/parties/<int:party_id>', methods=['PATCH'])
@login_required
def update_party(party_id):
    ''' Route to update party '''
    data = None
    response = {
        'status': 400,
        'error': 'Provide name, hq_address, logo_url and description as json.'
    }
    try:
        data = request.get_json()
    except:
        return make_response(jsonify(response), 400)
    if not data:
        return make_response(jsonify(response), 400)

    valid_keys = ['name', 'hq_address', 'logo_url', 'description']
    party_data = {}
    for key in valid_keys:
        party_data[key] = data.get(key)
    valdiator_result = Validator.validate_party(party_data)
    if isinstance(valdiator_result, dict):
        return make_response(jsonify(valdiator_result), valdiator_result['status'])
    if isinstance(valdiator_result, bool) and valdiator_result:
        party = politico.update_resource('party', party_id, party_data)

    response = {}
    if isinstance(party, Party):
        response['status'] = 200
        response['data'] = []
        response['data'].append({
            'id': party.id,
            'name': party.name
        })
    elif party == 'Party not found':
        response['status'] = 404
        response['error'] = 'Party not found'
    return make_response(jsonify(response), response['status'])

@party_blueprint.route('/parties/<int:party_id>', methods=['DELETE'])
@login_required
def delete_party(party_id):
    ''' Route to delete a party '''
    result = politico.delete_resource('party', party_id)
    response = {}
    if result == 'Party deleted':
        response['status'] = 202
        response['data'] = []
        response['data'].append({
            'message': 'Party deleted successfully'
        })
    elif result == 'Party not found':
        response['status'] = 404
        response['error'] = 'Party not found'
    return make_response(jsonify(response), response['status'])
