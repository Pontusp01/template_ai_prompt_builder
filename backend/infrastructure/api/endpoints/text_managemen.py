from flask import Blueprint, jsonify, request
import traceback
import sys


text_management_routes = Blueprint('text_management_routes', __name__)
text_management_service = TextManagementService()

@text_management_routes.route('/variables', methods=['GET'])
def get_variables():
    variables = text_management_service.get_all_variables()
    return jsonify(variables)

@text_management_routes.route('/variables', methods=['POST'])
def create_variable():
    variable_data = request.json
    variable = text_management_service.create_variable(variable_data)
    return jsonify(variable), 201

@text_management_routes.route('/variables/<int:variable_id>', methods=['GET'])
def get_variable(variable_id):
    variable = text_management_service.get_variable_by_id(variable_id)
    if variable:
        return jsonify(variable)
    else:
        return jsonify({'error': 'Variable not found'}), 404

@text_management_routes.route('/variables/<int:variable_id>', methods=['PUT'])
def update_variable(variable_id):
    variable_data = request.json
    updated_variable = text_management_service.update_variable(variable_id, variable_data)
    if updated_variable:
        return jsonify(updated_variable)
    else:
        return jsonify({'error': 'Variable not found'}), 404

@text_management_routes.route('/variables/<int:variable_id>', methods=['DELETE'])
def delete_variable(variable_id):
    deleted = text_management_service.delete_variable(variable_id)
    if deleted:
        return '', 204
    else:
        return jsonify({'error': 'Variable not found'}), 404