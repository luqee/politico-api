from flask import Blueprint, make_response, request, jsonify, g
from app.api.v1.models.office import Office
from app import politico
from app.api.v1.blueprints.validator import Validator
from app.api.v1.blueprints.decorators import login_required

office_blueprint = Blueprint('offices', __name__, url_prefix='/api/v1')

@office_blueprint.route('/offices', methods=['POST'])
@login_required
def create_office():
    ''' Route to create an office '''
    data = None
    response = {
        'status': 400,
        'error': 'Provide name, office_type, and description as json'
    }

    try:
        data = request.get_json()
    except:
        return make_response(jsonify(response), 400)
    if not data:
        return make_response(jsonify(response), 400)

    office_data = {
        'name': data.get('name'),
        'office_type': data.get('office_type'),
        'description': data.get('description')
    }
    valdiator_result = Validator.validate_office(office_data)
    if isinstance(valdiator_result, dict):
        return jsonify(valdiator_result), valdiator_result['status']
    if isinstance(valdiator_result, bool) and valdiator_result:
        result = politico.create_resource(g.user, office_data, 'office')

    response = {}
    if isinstance(result, Office):
        response['status'] = 201
        response['data'] = []
        response['data'].append({
            'id': result.id,
            'type': result.type,
            'name': result.name
        })
    elif result == 'Forbiden':
        response['status'] = 403
        response['error'] = 'You need to be an admin to create an office'
    elif result == 'Office exists':
        response['status'] = 409
        response['error'] = 'Office exists'
    return make_response(jsonify(response), response['status'])

@office_blueprint.route('/offices/<int:office_id>', methods=['GET'])
def get_office(office_id):
    ''' Route to get specific office '''
    office = politico.get_resource_by_id(office_id, 'office')
    response = {}
    if office == 'Not found':
        response['status'] = 404
        response['error'] = 'Office not found'
    elif isinstance(office, Office):
        response['status'] = 200
        response['data'] = []
        response['data'].append({
            'id': office.id,
            'type': office.type,
            'name': office.name
        })
    return make_response(jsonify(response), response['status'])

@office_blueprint.route('/offices', methods=['GET'])
def get_offices():
    ''' Route to get all offices '''
    offices = politico.get_offices()
    response = {}
    if isinstance(offices, list):
        response['status'] = 200
        response['data'] = []
        for office in offices:
            response['data'].append({
                'id': office.id,
                'type': office.type,
                'name': office.name
            })
        return make_response(jsonify(response), 200)

@office_blueprint.route('/offices/<int:office_id>', methods=['PATCH'])
@login_required
def update_office(office_id):
    ''' Route to update an office '''
    data = None
    response = {
        'status': 400,
        'error': 'Provide name, office_type, and description as json'
    }
    try:
        data = request.get_json()
    except:
        return make_response(jsonify(response), 400)
    if not data:
        return make_response(jsonify(response), 400)
    valid_keys = ['name', 'office_type', 'description']
    office_data = {}
    for key in valid_keys:
        office_data[key] = data.get(key)
    valdiator_result = Validator.validate_office(office_data)
    if isinstance(valdiator_result, dict):
        return jsonify(valdiator_result), valdiator_result['status']
    if isinstance(valdiator_result, bool) and valdiator_result:
        office = politico.update_resource('office', office_id, office_data)
    response = {}
    if isinstance(office, Office):
        response['status'] = 200
        response['data'] = []
        response['data'].append({
            'id': office.id,
            'name': office.name
        })
    elif office == 'Office not found':
        response['status'] = 404
        response['error'] = 'Office not found'
    return make_response(jsonify(response), response['status'])

@office_blueprint.route('/offices/<int:office_id>', methods=['DELETE'])
@login_required
def delete_office(office_id):
    ''' Route to delete an office '''
    result = politico.delete_resource('office', office_id)
    response = {}
    if result == 'Office deleted':
        response['status'] = 202
        response['data'] = []
        response['data'].append({
            'message': 'Office deleted successfully'
        })
    elif result == 'Office not found':
        response['status'] = 404
        response['error'] = 'Office not found'
    return make_response(jsonify(response), response['status'])
