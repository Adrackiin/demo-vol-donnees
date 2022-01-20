import os
import re


def file_is_present(file_name):
    try:
        fich = open(file_name, "rb")
        fich.close()
        return True
    except:
        return False


def path_is_correct(path):
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
    if base == '.':
        base = os.getcwd()
    path = re.sub("/+", '/', go_to if go_to != "" and go_to[0] == '/' else base + '/' + go_to)
    path_directories = [""]
    for directory in path.split('/'):
        if directory == '..':
            path_directories.pop()
            if len(path_directories) <= 0:
                path_directories.append("")
        elif directory != '.':
            path_directories.append(directory)
    return "/".join(path_directories)
