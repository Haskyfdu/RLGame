import requests
from flask import Flask, Blueprint, jsonify, request, send_from_directory

from HIVE.project_config import ProjectConfig

blueprint_main = Blueprint(name='blueprint_main', import_name=__name__)


@blueprint_main.route('/HIVE', methods=['GET'])
def view_game():
    if request.method == 'GET':
        return send_from_directory(ProjectConfig.Path['Templates_Path'], 'HIVE.html')


@blueprint_main.route('/ValidPlace', methods=['GET', 'POST'])
def get_valid_place_action():
    if request.method == 'GET':
        return jsonify('ValidPlace algorithm is online')
    else:
        message = request.get_json()
        pieces, destination = None, message
        return jsonify({'Pieces': pieces, 'Destination': destination})
