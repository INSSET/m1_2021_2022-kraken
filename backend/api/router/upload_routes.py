import os
import pathlib
import pwd
from _csv import reader

from flask import request, abort, Response, json, Blueprint

upload_routes = Blueprint('upload_routes', __name__)


@upload_routes.route('/api/upload/', methods=['POST'])
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def upload():
    global response
    path = pathlib.Path().absolute()
    request_data = json.dumps(request.get_json())
    data = json.loads(request_data)
    uploaded_key = data["key"].encode()
    user_name = data["user"].encode()
    student_path = str(path) + '/../etudiants/' + user_name + '/.ssh'
    sftp_path = str(path) + '/../etudiants/' + user_name + '/sftp/.ssh'
    user = pwd.getpwnam(user_name)
    user_id = user.pw_uid
    try:
        if not os.path.exists(student_path):
            os.makedirs(student_path)
            with open(os.path.join(student_path + '/authorized_keys'), 'x') as key_file:
                key_file.write(uploaded_key)
                response = {
                    'message': 'Clé ajoutée !',
                    'icon': 'mdi-check-circle',
                    'color': 'success'
                }
            os.chown(os.path.join(student_path + '/authorized_keys'), user_id, os.getuid())
        elif not os.path.exists(sftp_path):
            os.makedirs(sftp_path)
            with open(os.path.join(sftp_path + '/authorized_keys'), 'x') as key_file:
                key_file.write(uploaded_key)
                response = {
                    'message': 'Clé ajoutée ! (sftp)',
                    'icon': 'mdi-check-circle',
                    'color': 'success'
                }
            os.chown(os.path.join(sftp_path + '/authorized_keys'), user_id, os.getuid())
        elif not os.path.isfile(student_path + '/authorized_keys'):
            new_key_file = open(os.path.join(student_path + '/authorized_keys'), 'x')
            new_key_file.write(uploaded_key)
            response = {
                'message': 'Clé ajoutée !',
                'icon': 'mdi-check-circle',
                'color': 'success'
            }
            os.chown(os.path.join(student_path + '/authorized_keys'), user_id, os.getuid())
        elif not os.path.isfile(sftp_path + '/authorized_keys'):
            new_key_file = open(os.path.join(sftp_path + '/authorized_keys'), 'x')
            new_key_file.write(uploaded_key)
            response = {
                'message': 'Clé ajoutée ! (sftp)',
                'icon': 'mdi-check-circle',
                'color': 'success'
            }
            os.chown(os.path.join(sftp_path + '/authorized_keys'), user_id, os.getuid())
        else:
            student_file = open(os.path.join(student_path + '/authorized_keys'), 'r+')
            student_lines = student_file.readlines()
            student_stripped_lines = [k.rstrip() for k in student_lines]

            sftp_file = open(os.path.join(sftp_path + '/authorized_keys'), 'r+')
            sftp_lines = sftp_file.readlines()
            sftp_stripped_lines = [k.rstrip() for k in sftp_lines]
            if uploaded_key.rstrip() in student_stripped_lines and uploaded_key.rstrip() in sftp_stripped_lines:
                response = {
                    'message': 'Tu as déjà ajouté cette clé !',
                    'icon': 'mdi-alert-decagram',
                    'color': 'error'
                }
            elif uploaded_key.rstrip() not in student_stripped_lines:
                student_file.write(uploaded_key)
                response = {
                    'message': 'Une nouvelle clé a été ajoutée !',
                    'icon': 'mdi-check-circle',
                    'color': 'success'
                }
                os.chown(os.path.join(student_path + '/authorized_keys'), user_id, os.getuid())
            elif uploaded_key.rstrip() not in sftp_stripped_lines:
                sftp_file.write(uploaded_key)
                response = {
                    'message': 'Une nouvelle clé a été ajoutée ! (sftp)',
                    'icon': 'mdi-check-circle',
                    'color': 'success'
                }
                os.chown(os.path.join(sftp_path + '/authorized_keys'), user_id, os.getuid())
        return Response(json.dumps(response), mimetype='application/json', status=201)

    except KeyError:
        if not pwd.getpwnam(user_name):
            abort(404)
        else:
            abort(500)


@upload_routes.route('/api/upload-users-list/', methods=['POST'])
def upload_users_list():
    global response
    request_data = json.dumps(request.get_json())
    data = json.loads(request_data)
    users = data["users"].encode()
    group_id = data["groupId"].encode()
    data_file = open('./data.txt', 'w')
    data_file.write(users)
    data_file.close()
    with open('./data.txt', 'r') as users_list:
        csv_reader = reader(users_list)
        header = next(csv_reader)
        for line in csv_reader:
            user_name = line[6].split('@')
            if not user_name[0].startswith('harold'):
                shell = "/bin/bash"
                skelpath = "../conf/skel"
                path = pathlib.Path().absolute()
                student_dir_path = str(path) + '/../etudiants/'
                if not os.path.exists(student_dir_path):
                    os.makedirs(student_dir_path)
                try:
                    if user_name[0] in pwd.getpwnam(user_name[0]):
                        print('exists ' + user_name[0])
                except KeyError:
                    if not os.path.exists(student_dir_path):
                        os.makedirs(student_dir_path)

                    os.system("useradd -d /../etudiants/%s -K UID_MIN=10002 -m --skel %s -g %s -N --shell %s %s" % (
                        user_name[0], skelpath, group_id, shell, user_name[0]))
                    os.system("usermod -p '*' %s" % user_name[0])
                    os.system("usermod -a -G %s %s" % (group_id, user_name[0]))
                    os.system("chown root:root /../etudiants/%s" % user_name[0])

                    response = {
                        'message': 'Liste mise à jour !',
                        'icon': 'account-multiple-plus',
                        'color': 'success'
                    }
    os.remove('./data.txt')
    return Response(json.dumps(response), mimetype='application/json', status=201)
