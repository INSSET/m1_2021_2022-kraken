import json
import os
import pwd
import sys

from flask import Blueprint, Response, abort, request
import sys

from api.model.user import User
from api.utils.json_encoder import Encoder
import gestprojlib as GP
from api.model.user import User
from api.utils.json_encoder import Encoder

sys.path.append("/usr/src/app/gplib")

sys.path.append("/usr/src/app/gplib")

users_routes = Blueprint("users_routes", __name__)


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
        abort(404, description="Resources not found")


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
    liste = GP.liste_etudiant_group(group_name)
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

