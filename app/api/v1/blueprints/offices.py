from flask import Blueprint, request, jsonify, g
from app.api.v1.models.office import Office
from app import politico
from .decorators import login_required
from app.api.v1.blueprints.validator import Validator

office_blueprint = Blueprint('offices', __name__, url_prefix='/api/v1')

@office_blueprint.route('/offices', methods=['POST'])
@login_required
def create_office():
    data = request.get_json()
    
    office_data = {
        'name': data['name'],
        'office_type': data['type'],
        'description': data['description']
    }
    if Validator.validate_party(office_data):
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
    elif result == 'Not authorised':
        response = {
            'status': 403,
            'error': 'You need to be an admin to create an office'
        }
        return jsonify(response), 403
    elif result == 'Office exists':
        response = {
            'status': 406,
            'error': 'Office exists'
        }
        return jsonify(response), 406

@office_blueprint.route('/offices/<int:office_id>', methods=['GET'])
def get_office(office_id):
    office = politico.get_office_by_id(office_id)
    if office == 'Not found':
        response = {
            'status': 404,
            'error': 'Party not found'
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

@office_blueprint.route('/offices/<int:office_id>/name', methods=['PATCH'])
@login_required
def update_office(office_id):
    name = request.get_json()['name']
    office = politico.update_office(office_id, name)
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
def delete_party(office_id):
    result = politico.delete_office(office_id)
    if result == 'Office deleted':
        response = {
            'status': 200,
            'data':[]
        }
        response['data'].append({
            'message': 'Office deleted successfully'
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