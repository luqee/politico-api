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