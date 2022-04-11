import grp
import json

from flask import Blueprint, Response, abort, request

from model.group import Group
from utils.json_encoder import Encoder
from backend.gplib import gestprojlib

groups_routes = Blueprint('groups_routes', __name__)


@groups_routes.route('/api/v1/groups', methods=['GET'])
def get_groups():
    """ Retourne les noms et ids des groupes dont l'id est supérieur à 10000
    ainsi qu'un tableau avec la liste de tous les users appartenant au group """

    groups = []
    for group in grp.getgrall():
        if 10000 <= group.gr_gid < 20000:
            groups.append(Group(
                group.gr_gid,
                group.gr_name,
                group.gr_mem
            ))

    if len(groups) == 0:
        return Response('Groups not found', status=404, mimetype='application/json')

    encoded_groups = json.dumps(groups, cls=Encoder)

    return Response(encoded_groups, mimetype='application/json', status=200)


@groups_routes.route('/api/v1/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """ Retourne les informations d'un group
    L'id du group concerné est spécifié dans l'url <int:grp_id>
    Code 404 renvoyé en cas où le group n'existe pas"""

    try:
        group_trouve = grp.getgrgid(group_id)
        group = Group(
            group_trouve.gr_gid,
            group_trouve.gr_name,
            group_trouve.gr_mem
        )
        encoded_group = json.dumps(group, cls=Encoder)

        return Response(encoded_group, mimetype='application/json', status=200)
    except KeyError:
        abort(404, description='Not found - Could not find group with ID ' + group_id)


@groups_routes.route('/api/v1/groups', methods=['POST'])
def create_group():
    request_data = request.get_json()
    group_name = request_data['groupName'].encode()

    try:
        gestprojlib.create_group(group_name)
        return Response(mimetype='application/json', status=201)
    except KeyError:
        abort(500, description='Internal server error')


@groups_routes.route('/api/v1/groups/<int:group_id>', methods=['PATCH'])
def patch_group(group_id):
    request_data = request.get_json()
    group_name = request_data['groupName'].encode()

    if group_name == '':
        return Response('Bad request - Missing mandatory input value', mimetype='application/json', status=400)

    try:
        group = grp.getgrgid(group_id)

        os.system('groupmod -n ' + group_name + ' ' + group.group_name)

        return Response('Group with ID ' + group_id + ' has been updated', mimetype='application/json', status=200)
    except KeyError:
        abort(404, description='Not found - Could not find group with ID ' + group_id)


@groups_routes.route('/api/v1/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    try:
        group = grp.getgrgid(group_id)

        os.system('groupdel ' + group)

        return Response('Group with ID ' + group_id + ' has been deleted', mimetype='application/json', status=200)
    except KeyError:
        abort(404, description='Not found - Could not find group with ID ' + group_id)
