from flask import Blueprint, request, jsonify, g
from app.api.v1.models.office import Office
from app import politico
from .decorators import login_required
from app.api.v1.blueprints.validator import Validator

office_blueprint = Blueprint('offices', __name__, url_prefix='/api/v1')

@office_blueprint.route('/offices', methods=['POST'])
@login_required
def create_office():
    data = None
    try:
        data = request.get_json()
    except:
        response = {
            'status': 400,
            'error': 'Provide name, office_type, and description as json'
        }
        return jsonify(response), 400
    if not data:
        response = {
            'status': 400,
            'error': 'Provide name, office_type, and description as json'
        }
        return jsonify(response), 400
        
    office_data = {
        'name': data.get('name'),
        'office_type': data.get('office_type'),
        'description': data.get('description')
    }
    valdiator_result = Validator.validate_office(office_data)
    if isinstance(valdiator_result, dict):
        return jsonify(valdiator_result), valdiator_result['status']
    elif isinstance(valdiator_result, bool) and valdiator_result:
        result = politico.create_office(g.user, office_data)
    if type(result) == Office:
        response = {
            'status': 201,
            'data':[{
                'id': result.id,
                'type': result.type,
                'name': result.name
            }]
        }
        return jsonify(response), 201
    elif result == 'Forbiden':
        response = {
            'status': 403,
            'error': 'You need to be an admin to create an office'
        }
        return jsonify(response), 403
    elif result == 'Office exists':
        response = {
            'status': 409,
            'error': 'Office exists'
        }
        return jsonify(response), 409

@office_blueprint.route('/offices/<int:office_id>', methods=['GET'])
def get_office(office_id):
    office = politico.get_office_by_id(office_id)
    if office == 'Not found':
        response = {
            'status': 404,
            'error': 'Office not found'
        }        
        return jsonify(response), 404
    if type(office) == Office:
        response = {
            'status': 200,
            'data':[]
        }
        response['data'].append({
            'id': office.id,
            'type': office.type,
            'name': office.name
        })
        return jsonify(response), 200

@office_blueprint.route('/offices', methods=['GET'])
def get_offices():
    offices = politico.get_offices()
    if type(offices) == list:
        response = {
            'status': 200,
            'data':[]
        }
        for office in offices:
            response['data'].append({
                'id': office.id,
                'type': office.type,
                'name': office.name
            })
        return jsonify(response), 200

@office_blueprint.route('/offices/<int:office_id>', methods=['PATCH'])
@login_required
def update_office(office_id):
    data = None
    try:
        data = request.get_json()
    except:
        response = {
            'status': 400,
            'error': 'Provide name, office_type, and description as json'
        }
        return jsonify(response), 400
    if not data:
        response = {
            'status': 400,
            'error': 'Provide name, office_type, and description as json'
        }
        return jsonify(response), 400
    valid_keys = ['name', 'office_type','description']
    office_data = {}
    for key in valid_keys:
        office_data[key] = data.get(key)
    valdiator_result = Validator.validate_office(office_data)
    if isinstance(valdiator_result, dict):
        return jsonify(valdiator_result), valdiator_result['status']
    elif isinstance(valdiator_result, bool) and valdiator_result:
        office = politico.update_office(office_id, office_data)
    
    if type(office) == Office:
        response = {
            'status': 200,
            'data':[]
        }
        response['data'].append({
            'id': office.id,
            'name': office.name
        })
        return jsonify(response), 200
    elif office == 'Office not found':
        response = {
            'status': 404,
            'data':[{
                'error': 'Office not found'
            }]
        }
        return jsonify(response, 404)

@office_blueprint.route('/offices/<int:office_id>', methods=['DELETE'])
@login_required
def delete_office(office_id):
    result = politico.delete_office(office_id)
    if result == 'Office deleted':
        response = {
            'status': 202,
            'data':[]
        }
        response['data'].append({
            'message': 'Office deleted successfully'
        })
        return jsonify(response), 202
    elif result == 'Office not found':
        response = {
            'status': 404,
            'data':[{
                'error': 'Office not found'
            }]
        }
        return jsonify(response, 404)
