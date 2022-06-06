import click
import gestprojmail
import grp
import os
import getopt
import gestprojlib as gp
import sys

def success(message):
    click.echo(click.style(message, fg='green'))

def error(message):
    click.echo(click.style(message, fg='red'))

def warning(message):
    click.echo(click.style(message, fg='yellow'))

@click.group()
def main():
    pass

@click.group()
def add():
    pass

@click.group()
def rm():
    pass


@click.command(name='group')
@click.argument('group')
@click.argument('file')
def createGroup(group, file):
    try:
        info_grp = grp.getgrnam(group)
        error("Le Groupe %s existe deja %d " % (info_grp.gr_name, info_grp.gr_gid))
        sys.exit()
    except KeyError:
        initializedList = gp.initStudentListFromFile(file)
        gp.createGroup(group)
        gp.createUsers(initializedList, group)
        success("Le groupe %s a été créé avec succès." % group)
    return

@click.command(name='group')
@click.argument('group')
def deleteGroup(group):
    gp.deleteGroup(group)
    success("Le groupe %s a été supprimé avec succès." % group)
    return

@click.command(name='container')
@click.argument('action')
@click.option('--group', required=True, help='Groupe')
@click.option('--student', required=False, help='User')
@click.option('--type', required=False, help='Specify the type of docker you want to start (ex: symfony, icecode, mysql, etc...)')
@click.option('--container', required=False, help='Container')
def container(action, group, student, type, container):

    if group is not None and student is not None:

        if action == "logs":

            if container is None:
                error("Merci de spécifier un conteneur si vous voulez afficher ses logs (ex: Symfony -> [app|nginx])")
                sys.exit()

            containerInformations = gp.getStudentContainerInformations(group, student, container)
            gp.getContainerLogs(containerInformations['id'])
            sys.exit()

        try:
            gp.executeContainerActionForAStudent(action, student, group, type)
        except Exception as exception:
            error(str(exception))

    if group is not None and student is None:

        if action == "logs":
            error("Merci de spécifier un étudiant pour afficher les logs de son conteneur")
            sys.exit()

        try:
            gp.executeContainerActionForTheGroup(action, group, type)
        except Exception as exception:
            error(str(exception))

    return

@click.command(name='student')
@click.argument('action')
@click.argument('login')
@click.option('--ssh-key', 'sshKey', required=False, help='SSH File')
def student(action, login, sshKey):

    if action == "update":

        if sshKey is not None:

            isFile = True

            if os.path.exists(sshKey) is not True:
                isFile = False
                warning("Vous venez de propager une clé SSH en version string. Veillez à bien vérifier la validité de cette clé.")

            try:
                gp.updateAndPropagateSshKeys(login, sshKey, isFile)
                success("La propagation de la clé SSH de l'utilisateur %s a été faite avec succès" % login)
            except Exception as exception:
                error(str(exception))

    return

@click.command(name='test')
def test():
    print(gp.getSshPortFromPool())

# Init commands
main.add_command(add)
main.add_command(rm)
main.add_command(container)
main.add_command(test)
main.add_command(student)

# Add
add.add_command(createGroup)

# Remove
rm.add_command(deleteGroup)

main()