import grp
import json
import os
import sys

from flask import Blueprint, Response, abort, request

from model.group import Group
from utils.json_encoder import Encoder

groups_routes = Blueprint('groups_routes', __name__)

@groups_routes.route('/api/groups/', methods=['GET'])
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
    encoded_groups = json.dumps(groups, cls=Encoder)

    return Response(encoded_groups, mimetype='application/json', status=200)


@groups_routes.route('/api/groups/<int:group_id>/', methods=['GET'])
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
        abort(404, description="Resource not found")


@groups_routes.route('/api/create-groups/', methods=['POST'])
def create_group():
    request_data = request.get_json()
    encrypted_group_name = request_data['groupName']
    group_name = encrypted_group_name.encode()
    try:
        if grp.getgrnam(group_name):
            response = {
                'message': 'Ce groupe existe déjà !',
                'icon': 'mdi-alert-decagram',
                'color': 'error'
            }
            return Response(json.dumps(response), mimetype='application/json', status=409)
    except KeyError:
        os.system("groupadd -K GID_MIN=10001 %s" % group_name)

        return Response(mimetype='application/json', status=201)
