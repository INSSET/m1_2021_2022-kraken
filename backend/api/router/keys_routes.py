import json
import os
import pathlib
import pwd

from flask import Blueprint, Response

keys_routes = Blueprint('keys_routes', __name__)

@keys_routes.route('/api/keys/<int:user_id>/', methods=['GET'])
def get_keys(user_id):
    dir_path = pathlib.Path().absolute()
    user = pwd.getpwuid(user_id)
    user_name = user.pw_name
    key_file_path = str(dir_path) + '/../etudiants/' + user_name + '/.ssh/'
    if not os.path.isfile(os.path.join(key_file_path + '/authorized_keys')):
        response = {
            'message': 'Not found'
        }
        return Response(json.dumps(response), mimetype='application/json', status=404)
    key_file = open(os.path.join(key_file_path + '/authorized_keys'), 'r')
    keys = key_file.readlines()
    key_part = []
    for key in keys:
        divided_key = key.split("/")
        key_part.append(divided_key[1][0:10])
    return Response(json.dumps(key_part), mimetype='application/json', status=200)


@keys_routes.route('/api/keys/sftp/<int:user_id>/', methods=['GET'])
def get_sftp_keys(user_id):
    dir_path = pathlib.Path().absolute()
    user = pwd.getpwuid(user_id)
    user_name = user.pw_name
    sftp_key_file_path = str(dir_path) + '/../etudiants/' + user_name + '/sftp/.ssh/'
    if not os.path.isfile(os.path.join(sftp_key_file_path + '/authorized_keys')):
        response = {
            'message': 'Not found'
        }
        return Response(json.dumps(response), mimetype='application/json', status=404)
    key_file = open(os.path.join(sftp_key_file_path + '/authorized_keys'), 'r')
    keys = key_file.readlines()
    key_part = []
    for key in keys:
        divided_key = key.split("/")
        key_part.append(divided_key[1][0:10])
    return Response(json.dumps(key_part), mimetype='application/json', status=200)

