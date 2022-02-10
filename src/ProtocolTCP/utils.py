import os
import re


def file_is_present(file_name):
    """
    Renvoie vrai si le fichier est présent
    """
    try:
        fich = open(file_name, "rb")
        fich.close()
        return True
    except:
        return False


def path_is_correct(path):
    """
    Renvoie vrai si le chemin aboslu est correct
    """
    current = ""
    for directory in path.split('/'):
        current += '/' + directory
        if not os.path.isdir(current):
            return False
    return True


def get_path(base, go_to):
    """
    Construit le chemin complet pour atteindre un fichier à partir
    - soit d'un chemin relatif
    - soit d'un chemin absolu
    """
    # . correspond au dossier d'exécution
    if base == '.':
        base = os.getcwd()
    # Évite plusieurs / à la suite
    path = re.sub("/+", '/', go_to if go_to != "" and go_to[0] == '/' else base + '/' + go_to)
    # Liste des sous dossiers
    path_directories = []
    for directory in path.split('/'):
        # On remonte
        if directory == '..':
            if len(path_directories) > 0:
                path_directories.pop()
        # Si le dossier est '.', on ne fait rien car c'est le dossier actuel
        elif directory != '.':
            path_directories.append(directory)
    return "/".join(path_directories)


def parse_command(command):
    """
    Découpe une commande en action et arguments
    Les séparateurs sont des espaces, sauf s'il y a un '\' devant
    """
    args = command.strip().split(' ')
    result = []
    current_arg = []
    for arg in args:
        # Espace qui ne sépare pas les arguments
        if arg[-1] == "\\" and arg[-2] != "\\":
            current_arg.append(arg[:-1])
        else:
            current_arg.append(arg)
            result.append(" ".join(current_arg).replace("\\\\", "\\"))
            current_arg = []
    if len(current_arg) != 0:
        result.append(" ".join(current_arg).replace("\\\\", "\\"))
    return result
