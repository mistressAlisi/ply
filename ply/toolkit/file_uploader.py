import ply,os,errno,boto3,io,pathlib,os
def get_temp_path(path,profile):
    uuid = str(profile.uuid)
    relpath = f"{uuid[0]}/{uuid[1]}/{uuid[2]}/{uuid}/"
    return relpath+path
           
def save_temp_file(file,profile,name=False):
    if not name:
        path = get_temp_path(file.name,profile)
        pl = pathlib.Path(os.path.realpath(file.name))
        name = pl.name
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
        #print(os.path.realpath(file.name))
        pl = pathlib.Path(os.path.realpath(file.name))
        name = pl.stem
        path = get_temp_path(file.name,profile)
    if (ply.settings.PLY_AVATAR_STORAGE_USE_S3 == 'TRUE'):
        client = boto3.client('s3',aws_access_key_id=ply.settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=ply.settings.AWS_SECRET_ACCESS_KEY,endpoint_url=ply.settings.AWS_S3_ENDPOINT_URL)
        try: 
            keystr= f'{ply.settings.PLY_GALLERY_FILE_BASE_PATH}/{path}'
            #print(keystr)
            cache = io.BytesIO()
            file.save(cache,file.format)
            cache.seek(0)
            client.put_object(Body=cache,ACL='public-read', Bucket=ply.settings.AWS_STORAGE_BUCKET_NAME, Key=keystr)
            bw = cache.tell()
            cache.close()
            return bw
        except:
            raise Exception('Unable to store Gallery File in S3 Storage')
    else:
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
                bw = destination.tell()
            destination.close()
        return bw

def save_original_file(file,profile,name=False):
    if not name:
        #print(os.path.realpath(file.name))
        pl = pathlib.Path(os.path.realpath(file.name))
        name = pl.name
        path = get_temp_path(name,profile)
    else:
        path = get_temp_path(name,profile)
    if (ply.settings.PLY_GALLERY_STORAGE_USE_S3 == 'TRUE'):
        client = boto3.client('s3',aws_access_key_id=ply.settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=ply.settings.AWS_SECRET_ACCESS_KEY,endpoint_url=ply.settings.AWS_S3_ENDPOINT_URL)
        try: 
            keystr= f'{ply.settings.PLY_GALLERY_ORIGINAL_FILE_BASE_PATH}/{path}'

            client.put_object(Body=file,ACL='public-read', Bucket=ply.settings.AWS_STORAGE_BUCKET_NAME, Key=keystr)
            bw = file.tell()
            return bw
        except:
            raise Exception('Unable to store Original File in S3 Storage')
    else:
        destpath = ply.settings.PLY_GALLERY_ORIGINAL_FILE_BASE_PATH+path
        if not os.path.exists(os.path.dirname(destpath)):
            try:
                os.makedirs(os.path.dirname(destpath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(destpath, 'wb+') as destination:
            #for chunk in file.chunks():
            destination.write(file.read())
            bw = destination.tell()
            destination.close()
        return bw


def save_avatar_file(file,profile,name=False):
    if not name:
        pl = pathlib.Path(os.path.realpath(file))
        path = get_temp_path(file.name,profile)
        name = pl.stem
    else:
        path = get_temp_path(name,profile)

    if (ply.settings.PLY_AVATAR_STORAGE_USE_S3 == 'TRUE'):
        client = boto3.client('s3',aws_access_key_id=ply.settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=ply.settings.AWS_SECRET_ACCESS_KEY,endpoint_url=ply.settings.AWS_S3_ENDPOINT_URL)
        try: 
            keystr= f'{ply.settings.PLY_AVATAR_FILE_BASE_PATH}/{name}'
            cache = io.BytesIO()
            file.save(cache,file.format)
            cache.seek(0)
            client.put_object(Body=cache,ACL='public-read', Bucket=ply.settings.AWS_STORAGE_BUCKET_NAME, Key=keystr)
            cache.close()
            return name
        except:
            raise Exception('Unable to store Avatar in S3 Storage')
    else:
        # Storage to hard drive:
        destpath = ply.settings.PLY_AVATAR_FILE_BASE_PATH+f"/{path}"
        if not os.path.exists(os.path.dirname(destpath)):
            try:
                os.makedirs(os.path.dirname(destpath))
            except OSError as exc: # Guard against race condition   
                if exc.errno != errno.EEXIST:
                    raise
        with open(destpath, 'wb+') as destination:
            try:
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
            except:
                file.save(destpath)
        return path


def get_original_file(name):
    if not name:
        return False
    destpath = ply.settings.PLY_GALLERY_ORIGINAL_FILE_BASE_PATH+"/"+name
    if (ply.settings.PLY_GALLERY_STORAGE_USE_S3 == 'TRUE'):
        client = boto3.client('s3',aws_access_key_id=ply.settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=ply.settings.AWS_SECRET_ACCESS_KEY,endpoint_url=ply.settings.AWS_S3_ENDPOINT_URL)
        try:
            f = io.BytesIO()
            client.download_fileobj(ply.settings.AWS_STORAGE_BUCKET_NAME, destpath, f)
            return f
        except Exception as e:
            raise Exception(f'Unable to store Read File from S3 Storage: {e}')
    else:
        if not os.path.exists(destpath):
            raise Exception(f'Path Not found: {destpath}')
        with open(destpath, 'rb+') as source:
            #for chunk in file.chunks():
            return source
