from flask import Blueprint, request, jsonify, g
from app.api.v1.models.office import Office
from app import politico
from .decorators import login_required

office_blueprint = Blueprint('offices', __name__, url_prefix='/api/v1')

@office_blueprint.route('/offices', methods=['POST'])
@login_required
def create_office():
    data = request.get_json()
    name = data['name']
    office_type = data['type']
    description = data['description']
    
    new_office = Office(name, office_type, description)
    result = politico.create_office(g.user, new_office)
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
            'status': 401,
            'error': 'You need to be an admin to create an office'
        }
        return jsonify(response), 401

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
    response = {
        'status': 400,
        'data':[]
    }

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
    response = {
        'status': 400,
        'data':[]
    }