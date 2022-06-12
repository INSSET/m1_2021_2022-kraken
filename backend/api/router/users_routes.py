import grp
import json
import os
import pathlib
import pwd
import sys
from os.path import exists

from flask import Blueprint, Response, abort, request

import gestprojlib
from api.model.user import User
from api.utils.json_encoder import Encoder

sys.path.append("/usr/src/app/gplib")

users_routes = Blueprint("users_routes", __name__)

containerType = 'symfony'
containerName = 'symfony-app'


@users_routes.route("/api/v1/students", methods=["OPTIONS"])
def preflight_get_users():
    """ Le front en VueJS execute une requête préliminaire pour vérifier la possibilité de faire un GET
    par défaut flask renvoie une redirection 302 qui n'est pas pris en charge par les navigateurs
    on renvoit ici 204 (No Content) pour valider le cross-origin comme prévu dans le protocole CORS"""
    return Response(response=None, status=204)


@users_routes.route("/api/v1/students/", methods=["GET"])
def get_users():
    """ Retourne l'id, le nom et l'id du group des users dont l'id est supérieur à 10000 """
    users = []
    for user in pwd.getpwall():
        if 10000 <= user.pw_uid < 20000:
            users.append(
                User(
                    user.pw_uid,
                    user.pw_name,
                    user.pw_gid
                ))
    encoded_users = json.dumps(users, cls=Encoder)

    return Response(encoded_users, mimetype="application/json", status=200)


@users_routes.route("/api/v1/students/<int:user_id>/", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user_trouve = pwd.getpwuid(user_id)
        user_id = str(user_trouve.pw_uid)
        user_name = str(user_trouve.pw_name)
        group_id = str(user_trouve.pw_gid)
        user = User(
            user_id,
            user_name,
            group_id
        )

        encoded_user = json.dumps(user, cls=Encoder)

        return Response(encoded_user, mimetype="application/json", status=200)
    except KeyError:
        abort(404, description='Not found - Could not find user with ID ' + user_id)


@users_routes.route('/api/v1/students/<int:user_id>/keys/', methods=['GET'])
def get_keys(user_id):
    dir_path = pathlib.Path().absolute()
    try:
        user = pwd.getpwuid(user_id)
        user_name = user.pw_name
        key_file_path = str(dir_path) + '/../../etudiants/' + user_name + '/.ssh/'
        if not os.path.isfile(os.path.join(key_file_path + '/authorized_keys')):
            return Response('Resource not found', mimetype='application/json', status=404)
        key_file = open(os.path.join(key_file_path + '/authorized_keys'), 'r')
        keys = key_file.readlines()
        key_part = []
        for key in keys:
            k = key.rstrip("\n")
            key_part.append(k)

        key_dict = {
            'keys': key_part
        }
        return Response(json.dumps(key_dict), mimetype='application/json', status=200)
    except KeyError:
        if not pwd.getpwuid(user_id):
            abort(404, description='Not found - Could not find user ID ' + user_id)
        else:
            abort(500, description='Internal server error - Something went wrong when retrieving ssh keys')


@users_routes.route("/api/v1/students/", methods=["POST"])
def create_user():
    try:
        request_data = request.get_json()
        user_firstname = request_data["firstname"]
        user_lastname = request_data["lastname"]
        user_name = user_firstname + "." + user_lastname
        if pwd.getpwnam(user_name):
            response = {
                "message": "L\'étudiant·e existe déjà !"
            }
            return Response(json.dumps(response), mimetype="application/json", status=409)
    except KeyError:
        request_data = request.get_json()
        user_firstname = request_data["firstname"]
        user_lastname = request_data["lastname"]
        user_group_name = request_data["groupName"]
        shell = "/bin/bash"
        skelpath = "../conf/skel"
        user_name = user_firstname + "." + user_lastname
        student_dir_path = "/home/etudiants/" + user_name
        os.makedirs(student_dir_path)

        os.system("useradd -d /home/etudiants/%s -K UID_MIN=10002 -m --skel %s -g %s -N --shell %s %s" % (
            user_name, skelpath, user_group_name, shell, user_name))
        os.system("usermod -p '*' %s" % user_name)
        os.system("usermod -a -G %s %s" % (user_group_name, user_name))
        os.system("chown root:root /home/etudiants/%s" % user_name)

        os.system("useradd -d /home/etudiants/%s/sftp -K UID_MIN=10002 --shell %s -N -g %s sftp.%s" % (
            user_name, shell, 'sftp', user_name))
        os.system("usermod -p '*' sftp.%s" % user_name)
        os.system("mkdir -p /home/etudiants/%s/sftp/Projets" % user_name)
        os.system("mkdir -p /home/etudiants/%s/sftp/.ssh" % user_name)
        os.system("chown root:root /home/etudiants/%s/sftp" % user_name)
        os.system("chown sftp.%s:sftp /home/etudiants/%s/sftp/Projets" % (user_name, user_name))
        os.system("chown sftp.%s:sftp /home/etudiants/%s/sftp/.ssh" % (user_name, user_name))
        os.system("chmod 775 /home/etudiants/%s/sftp/Projets" % user_name)

        return Response(mimetype="application/json", status=201)


@users_routes.route("/api/v1/students/group/<string:group_name>/", methods=["GET"])
def get_users_by_group(group_name):
    """
    Renvoie la liste de tous les utilisateurs appartenant au group "group_name"
    """
    liste = gestprojlib.liste_etudiant_group(group_name)
    return Response(json.dumps(liste, cls=Encoder), mimetype="application/json", status=200)


@users_routes.route('/api/v1/students/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = pwd.getpwuid(user_id)

        os.system('userdel -f --remove %s' % user.pw_name)
        os.system("userdel -f --remove sftp.%s" % user.pw_name)

        return Response('User ' + user.pw_name + ' has been deleted', mimetype='application/json', status=200)
    except KeyError:
        abort(404, description='Not found - Could not find user with ID ' + user_id)


@users_routes.route('/api/v1/students/<int:user_id>/ssh/upload/', methods=['POST'])
def upload(user_id):
    global response
    path = pathlib.Path().absolute()
    request_data = request.get_json()

    ssh_key = request_data["key"]

    try:
        user = pwd.getpwuid(user_id)
        student_path = str(path) + '/../../etudiants/' + user.pw_name + '/.ssh'
        sftp_path = str(path) + '/../../etudiants/' + user.pw_name + '/sftp/.ssh'

        # Check if authorized_keys file exists
        sftp_auth_file = exists(sftp_path + '/authorized_keys')
        if not sftp_auth_file:
            sftp_keys_file = open(sftp_path + '/authorized_keys', "x")
            sftp_keys_file.close()

        ssh_auth_file = exists(student_path + '/authorized_keys')
        if not ssh_auth_file:
            keys_file = open(student_path + '/authorized_keys', "x")
            keys_file.close()

        keyList = []
        # Check if the key is already stored in authorized_keys file
        with open(os.path.join(student_path + '/authorized_keys'), 'r') as ssh_file:
            for line in ssh_file.readlines():
                keyList.append(line.rstrip("\n"))

        # Check if the key is already stored in sftp authorized_keys file'
        sftpList = []
        with open(os.path.join(sftp_path + '/authorized_keys'), 'r') as sftp_file:
            for line in sftp_file.readlines():
                sftpList.append(line.rstrip("\n"))

        if ssh_key not in keyList and ssh_key not in sftpList:

            with open(os.path.join(student_path + '/authorized_keys'), 'a', newline="") as key_file:
                key_file.write(ssh_key + '\n')
                os.chown(os.path.join(student_path + '/authorized_keys'), user_id, os.getuid())

            print('ssh key added')

            with open(os.path.join(sftp_path + '/authorized_keys'), 'a', newline="") as key_file:
                key_file.write(ssh_key + '\n')
                os.chown(os.path.join(student_path + '/authorized_keys'), user_id, os.getuid())

            print('ssh key added to sftp')

            return Response('Key has been successfully uploaded', mimetype='application/json', status=200)
        else:
            return Response('Key has already been uploaded', mimetype='application/json', status=409)

    except KeyError:
        if not pwd.getpwuid(user_id):
            abort(404, description='Not found - Could not find user ID ' + user_id)
        else:
            abort(500, description='Internal server error - Something went wrong when writing ssh keys')


@users_routes.route('/api/v1/students/<int:user_id>/container/command/<string:action>', methods=['POST'])
def post_container_action(user_id, action):
    try:
        user = pwd.getpwuid(user_id)
        group = grp.getgrgid(user.pw_gid)
        gestprojlib.executeContainerActionForAStudent(action, user.pw_name, group.gr_name, containerType)

        return Response('Container command: ' + action + ', for ' + user.pw_name + ' has been executed',
                        mimetype='application/json', status=200)
    except KeyError:
        if not pwd.getpwuid(user_id):
            abort(404, description='Not found - Could not find user ID ' + user_id)
        else:
            abort(500, description='Internal server error - Something went wrong when executing container action')


@users_routes.route('/api/v1/students/<int:user_id>/container/info', methods=['GET'])
def get_student_container_info(user_id):
    try:
        user = pwd.getpwuid(user_id)
        group = grp.getgrgid(user.pw_gid)
        return Response(
            json.dumps(gestprojlib.getStudentContainerInformations(group.gr_name, user.pw_name, containerName)),
            mimetype='application/json', status=200)
    except KeyError:
        if not pwd.getpwuid(user_id):
            abort(404, description='Not found - Could not find user ID ' + user_id)
        else:
            abort(500, description='Internal server error - Something went wrong when fetching container info')


@users_routes.route('/api/v1/students/<int:user_id>/dockerfile', methods=['GET'])
def get_student_dockerfile(user_id):
    try:
        user = pwd.getpwuid(user_id)
        group = grp.getgrgid(user.pw_gid)
        path = pathlib.Path().absolute()
        docker_file_lines = []
        f = open(
            str(path) + '/../.docker/' + group.gr_name + '/' + user.pw_name + '/' + containerType + '/php/Dockerfile',
            'r')
        for line in f.readlines():
            docker_file_lines.append(line)

        file = {
            'dockerFile': docker_file_lines
        }
        return Response(json.dumps(file), mimetype='application/json', status=200)
    except KeyError:
        if not pwd.getpwuid(user_id):
            abort(404, description='Not found - Could not find user ID ' + user_id)
        else:
            abort(500, description='Internal server error - Something went wrong when fetching Dockerfile')


@users_routes.route('/api/v1/students/<int:user_id>/dockerfile', methods=['POST'])
def update_student_dockerfile(user_id):
    try:
        user = pwd.getpwuid(user_id)
        group = grp.getgrgid(user.pw_gid)
        path = pathlib.Path().absolute()

        request_data = request.get_json()
        dockerFile = request_data["dockerFile"]

        f = open(
            str(path) + '/../.docker/' + group.gr_name + '/' + user.pw_name + '/' + containerType + '/php/Dockerfile',
            'w')
        for line in dockerFile:
            f.write(line)

        return Response(user.pw_name + ' Dockerfile has been updated', mimetype='application/json', status=200)
    except KeyError:
        if not pwd.getpwuid(user_id):
            abort(404, description='Not found - Could not find user ID ' + user_id)
        else:
            abort(500, description='Internal server error - Something went wrong when updating Dockerfile')
