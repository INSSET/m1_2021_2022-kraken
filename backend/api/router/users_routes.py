import json
import os
import pathlib
import pwd

from flask import Blueprint, Response, abort, request
from model.user import User
from utils.json_encoder import Encoder

import sys
sys.path.append("/usr/src/app/gplib")

import gestprojlib as GP

users_routes = Blueprint("users_routes", __name__)


@users_routes.route("/api/users", methods=["OPTIONS"])
def preflight_get_users():
    """ Le front en VueJS execute une requête préliminaire pour vérifier la possibilité de faire un GET
    par défaut flask renvoie une redirection 302 qui n'est pas pris en charge par les navigateurs
    on renvoit ici 204 (No Content) pour valider le cross-origin comme prévu dans le protocole CORS"""
    return Response(response=None, status=204)


@users_routes.route("/api/users/", methods=["GET"])
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


@users_routes.route("/api/users/<int:user_id>/", methods=["GET"])
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


@users_routes.route("/api/create-users/", methods=["POST"])
def create_user():
    try:
        request_data = request.get_json()
        user_firstname = request_data["firstname"]
        user_lastname = request_data["lastname"]
        user_name = user_firstname + "." + user_lastname
        if pwd.getpwnam(user_name):
            response = {
                "message": "L\'étudiant·e existe déjà !",
                "icon": "mdi-alert-decagram",
                "color": "error"
            }
            return Response(json.dumps(response), mimetype="application/json", status=409)
    except KeyError:
        request_data = request.get_json()
        user_firstname = request_data["firstname"]
        user_lastname = request_data["lastname"]
        user_group_id = int(request_data["groupId"])
        shell = "/bin/bash"
        skelpath = "../conf/skel"
        user_name = user_firstname + "." + user_lastname
        path = pathlib.Path().absolute()
        student_dir_path = str(path) + "/../home/etudiants/" + user_name
        os.makedirs(student_dir_path)

        os.system("useradd -d /home/etudiants/%s -K UID_MIN=10002 -m --skel %s -g %s -N --shell %s %s" % (
            user_name, skelpath, user_group_id, shell, user_name))
        os.system("usermod -p '*' %s" % user_name)
        os.system("usermod -a -G %s %s" % (user_group_id, user_name))
        os.system("chown root:root /home/etudiants/%s" % user_name)

        user = pwd.getpwnam(user_name)
        new_user = User(user.pw_uid, user.pw_name, user.pw_gid)
        encoded_user = json.dumps(new_user, cls=Encoder)

        return Response(encoded_user, mimetype="application/json", status=201)


@users_routes.route("/api/users/group/<string:group_name>/", methods=["GET"])
def get_users_by_group(group_name):
    """
    Renvoie la liste de tous les utilisateurs appartenant au group "group_name"
    """
    liste = GP.liste_etudiant_group(group_name)
    return Response(json.dumps(liste, cls=Encoder), mimetype="application/json", status=200)
