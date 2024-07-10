import ply, os, errno, boto3, io, pathlib, os
from django.core.files.storage import default_storage, storages

from ply.toolkit.logger import getLogger

logging = getLogger("toolkit.file_uploader", name="toolkit.file_uploader")


def get_file_path(path, profile):
    uuid = str(profile.uuid)
    relpath = f"{uuid[0]}/{uuid[1]}/{uuid[2]}/{uuid}/"
    return relpath + path



def save_temp_file(file, profile, name=False):
    if not name:
        path = get_file_path(file.name, profile)
        pl = pathlib.Path(os.path.realpath(file.name))
        name = pl.name
    else:
        path = get_file_path(name, profile)
    destpath = ply.settings.PLY_TEMP_FILE_BASE_PATH + path
    if not os.path.exists(os.path.dirname(destpath)):
        try:
            os.makedirs(os.path.dirname(destpath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(destpath, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    logging.info(
        f"Successfully stored Temporary File: {destpath}. Owner: {profile.uuid}"
    )
    return path


def save_gallery_file(file, profile, name=False):
    if not name:
        # print(os.path.realpath(file.name))
        pl = pathlib.Path(os.path.realpath(file.name))
        name = pl.name
        path = get_file_path(name, profile)
    else:
        path = get_file_path(name, profile)
    fullname = f"{path}"
    gstorages = storages["gallery_publish"]
    try:
        gstorages.delete(fullname)
    except:
        pass
    gstorages.save(fullname, file)
    size = gstorages.size(fullname)
    logging.info(
        f"Successfully stored Gallery File: {fullname}. Owner: {profile.uuid}. Size: {size}"
    )
    return path, size


def save_original_file(file, profile, name=False):
    if not name:
        # print(os.path.realpath(file.name))
        pl = pathlib.Path(os.path.realpath(file.name))
        name = pl.name
        path = get_file_path(name, profile)
    else:
        path = get_file_path(name, profile)
    fullname = f"{path}"
    gstorages = storages["gallery_originals"]
    try:
        gstorages.delete(fullname)
    except:
        pass
    gstorages.save(fullname, file)
    size = gstorages.size(fullname)
    logging.info(
        f"Successfully stored Gallery Original File: {fullname}. Owner: {profile.uuid}. Size: {size}"
    )
    return path, size


def save_avatar_file(file, profile, name=False):
    if not name:
        pl = pathlib.Path(os.path.realpath(file))
        path = get_file_path(file.name, profile)
        name = pl.stem
    else:
        path = get_file_path(name, profile)
    fullname = f"{path}"
    avstorages = storages["avatars"]
    try:
        avstorages.delete(fullname)
    except:
        pass
    avstorages.save(fullname, file)
    size = avstorages.size(fullname)
    logging.info(
        f"Successfully stored Avatar File: {fullname}. Owner: {profile.uuid}. Size: {size}"
    )
    return path, size


def get_original_file(name):
    if not name:
        return False
    gstorages = storages["gallery_originals"]
    if gstorages.exists(name):
        fileptr = gstorages.open(name)
        return fileptr
    else:
        return False
