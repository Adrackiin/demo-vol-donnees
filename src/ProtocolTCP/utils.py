def file_is_present(file_name):
    try:
        fich = open(file_name, "rb")
        fich.close()
        return True
    except:
        return False


def concatenate_path(current, move_to):
    if move_to != "" and move_to[0] == '/':
        return move_to
    return current + move_to
