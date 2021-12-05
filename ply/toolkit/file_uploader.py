import ply,os,errno
def get_temp_path(path,profile):
    uuid = str(profile.uuid)
    relpath = f"{uuid[0]}/{uuid[1]}/{uuid[2]}/{uuid}/"
    return relpath+path
           
def save_temp_file(file,profile,name=False):
    if not name:
        path = get_temp_path(file.name,profile)
    else:
        path = get_temp_path(name,profile)
    destpath = ply.settings.PLY_TEMP_FILE_BASE_PATH+path
    if not os.path.exists(os.path.dirname(destpath)):
        try:
            os.makedirs(os.path.dirname(destpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(destpath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    return path


def save_gallery_file(file,profile,name=False):
    if not name:
        path = get_temp_path(file.name,profile)
    else:
        path = get_temp_path(name,profile)
    destpath = ply.settings.PLY_GALLERY_FILE_BASE_PATH+path
    if not os.path.exists(os.path.dirname(destpath)):
        try:
            os.makedirs(os.path.dirname(destpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(destpath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    return path

def save_original_file(file,profile,name=False):
    if not name:
        path = get_temp_path(file.name,profile)
    else:
        path = get_temp_path(name,profile)
    destpath = ply.settings.PLY_GALLERY_ORIGINAL_FILE_BASE_PATH+path
    if not os.path.exists(os.path.dirname(destpath)):
        try:
            os.makedirs(os.path.dirname(destpath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(destpath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    return path
