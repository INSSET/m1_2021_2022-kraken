import grp
import json
import os

from flask import Blueprint, Response, abort, request

from model.group import Group
from utils.json_encoder import Encoder
import gestprojlib

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
    group_name = request_data['groupName']

    if group_name == '':
        return Response('Bad request - Missing mandatory input value', mimetype='application/json', status=400)

    try:
        gestprojlib.create_group(group_name)
        return Response(mimetype='application/json', status=201)
    except KeyError:
        abort(500, description='Internal server error')


@groups_routes.route('/api/v1/groups/<int:group_id>', methods=['PATCH'])
def patch_group(group_id):
    request_data = request.get_json()
    new_group_name = request_data['groupName']

    if new_group_name == '':
        return Response('Bad request - Missing mandatory input value', mimetype='application/json', status=400)

    try:
        group = grp.getgrgid(group_id)

        os.system('groupmod -n ' + new_group_name + ' ' + group.gr_name)

        return Response('Group with ID ' + str(group_id) + ' has been updated', mimetype='application/json', status=200)
    except KeyError:
        abort(404, description='Not found - Could not find group with ID ' + group_id)


@groups_routes.route('/api/v1/groups/<string:group_name>/upload', methods=['POST'])
def upload_group(group_name):
    try:
        grp.getgrnam(group_name)

        f = request.files['file']
        f.save('/tmp/' + f.filename)

        student_list = gestprojlib.init_liste('/tmp/' + f.filename)

        stored_users = gestprojlib.liste_etudiant_group(group_name)

        users_list = []
        students = []

        for users in stored_users:
            users_list.append(users.get('user')[0])

        for student in student_list:
            students.append(student.get('login'))

        for u in users_list:
            if u not in students:
                os.system('userdel -f --remove %s' % u)
                os.system("userdel -f --remove sftp.%s" % u)

        gestprojlib.create_users(student_list, group_name)

        gestprojlib.create_sftp_users(student_list)

        f.close()
        os.remove('/tmp/' + f.filename)

        return Response(mimetype='application/json', status=201)
    except KeyError:
        gestprojlib.create_group(group_name)

        f = request.files['file']
        f.save('/tmp/' + f.filename)
        student_list = gestprojlib.init_liste('/tmp/' + f.filename)

        gestprojlib.create_users(student_list, group_name)

        gestprojlib.create_sftp_users(student_list)

        f.close()
        os.remove('/tmp/' + f.filename)

        return Response(mimetype='application/json', status=201)

    # @groups_routes.route('/api/v1/groups/<string:group_name>/update', methods=['POST'])
    # def update_group(group_name):
    #     f = request.files['file']
    #     f.save('/tmp/' + f.filename)
    #     student_list = gestprojlib.init_liste('/tmp/' + f.filename)
    #
    #     stored_users = gestprojlib.liste_etudiant_group(group_name)
    #
    #     users_list = []
    #     new_students = []
    #
    #     for users in stored_users:
    #         users_list.append(users.get('user')[0])
    #
    #     for s in student_list:
    #         if s.get('login') not in users_list:
    #             new_students.append(s.get('login'))
    #
    #     gestprojlib.create_users(new_students, group_name)
    #
    #     gestprojlib.create_sftp_users(new_students)
    #
    #     for u in users_list:
    #         if u not in student_list:
    #             os.system('userdel -r ' + u)
    #             os.system('userdel -r ' + 'sftp.' + u)
    #
    #     f.close()
    #     os.remove('/tmp/' + f.filename)

    return Response(mimetype='application/json', status=201)


@groups_routes.route('/api/v1/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    try:
        group = grp.getgrgid(group_id)

        gestprojlib.sup_sftp_users(group.gr_name)
        gestprojlib.sup_group(group.gr_name)

        return Response('Group ' + group.gr_name + ' has been deleted', mimetype='application/json', status=200)
    except KeyError:
        abort(404, description='Not found - Could not find group with ID ' + group_id)
