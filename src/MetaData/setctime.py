import os

# https://github.com/Delgan/win32-setctime/blob/master/win32_setctime.py

try:
    from ctypes import byref, get_last_error, wintypes, FormatError, WinDLL, WinError

    # Utilisation des bibliothèques windows
    kernel32 = WinDLL("kernel32", use_last_error=True)

    # Créer un fichier (supporte l'unicode, contrairement à CreateFile)
    CreateFileW = kernel32.CreateFileW
    # Modifier les dates de création, modification et d'accès
    SetFileTime = kernel32.SetFileTime
    # Fermer un fichier
    CloseHandle = kernel32.CloseHandle

    # Définitions des types d'arguments et types de retours des fonctions windows
    CreateFileW.argtypes = (
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    CreateFileW.restype = wintypes.HANDLE

    SetFileTime.argtypes = (
        wintypes.HANDLE,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
    )
    SetFileTime.restype = wintypes.BOOL

    CloseHandle.argtypes = (wintypes.HANDLE,)
    CloseHandle.restype = wintypes.BOOL
except (ImportError, AttributeError, OSError, ValueError):
    # Pas exécuté sur Windows
    SUPPORTED = False
else:
    SUPPORTED = os.name == "nt"

__version__ = "1.0.3"
__all__ = ["setctime"]


def setctime(filepath, timestamp):
    """Set the "ctime" (creation time) attribute of a file given an unix timestamp (Windows only)."""
    if not SUPPORTED:
        return

    # Chemin absolu du fichier
    filepath = os.path.normpath(os.path.abspath(str(filepath)))
    # Conversion d'un horodatage du temps universel depuis le 1er janvier 1970, en horodatage windows
    # qui utilise le temps depuis le 1er janvier 1601
    # 1er janvier 1601 + 116444736000000000 = 1er janvier 1970
    # https://docs.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime
    timestamp = int((timestamp * 10000000) + 116444736000000000)

    # Vérification de l'horodatage
    if not 0 < timestamp < (1 << 64):
        raise ValueError("The system value of the timestamp exceeds u64 size: %d" % timestamp)

    # Conversion d'un horodatage de 64 bits en deux champs de 32 bits
    atime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
    mtime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)
    ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)

    # https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew
    handle = wintypes.HANDLE(CreateFileW( # Obtenir "handle"
        filepath, # Fichier
        256, # Permissions
        0, # Accès par d'autres processus, 0 = ne peuvent rien faire tant qu'il est ouvert
        None,
        3, # Ouvre un fichier seulement s'il existe
        128 | 0x02000000, # Obtenir "handle" sur répertoire
        None))
    if handle.value == wintypes.HANDLE(-1).value: # Erreur
        raise WinError(get_last_error())

    if not wintypes.BOOL(SetFileTime(handle, byref(ctime), byref(atime), byref(mtime))): # Modification des dates du ficher
        raise WinError(get_last_error())

    if not wintypes.BOOL(CloseHandle(handle)): # Fermeture du fichier
        raise WinError(get_last_error())
