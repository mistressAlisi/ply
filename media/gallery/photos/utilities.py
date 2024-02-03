import datetime
from fractions import Fraction
from PIL import Image
import PIL.ExifTags
from ply.toolkit import file_uploader
import ply
import os
def generate_exif_dict(image):

    """
    Generate a dictionary of dictionaries.

    The outer dictionary keys are the names
    of individual items, eg Make, Model etc.

    The outer dictionary values are themselves
    dictionaries with the following keys:

        tag: the numeric code for the item names
        raw: the data as stored in the image, often
        in a non-human-readable format
        processed: the raw data if it is human-readable,
        or a processed version if not.
    """

    try:


        exif_data_PIL = image._getexif()

        exif_data = {}

        for k, v in PIL.ExifTags.TAGS.items():

            if k in exif_data_PIL:
                value = exif_data_PIL[k]
            else:
                value = None

            if len(str(value)) > 64:
                value = str(value)[:65] + "..."

            exif_data[v] = {"tag": k,
                            "processed": value}


        exif_data = _process_exif_dict(exif_data)

        return exif_data

    except IOError as ioe:

        raise


def _derationalize(rational):

    return rational.numerator / rational.denominator


def _create_lookups():

    lookups = {}

    lookups["metering_modes"] = ("Undefined",
                                 "Average",
                                 "Center-weighted average",
                                 "Spot",
                                 "Multi-spot",
                                 "Multi-segment",
                                 "Partial")

    lookups["exposure_programs"] = ("Undefined",
                                    "Manual",
                                    "Program AE",
                                    "Aperture-priority AE",
                                    "Shutter speed priority AE",
                                    "Creative (Slow speed)",
                                    "Action (High speed)",
                                    "Portrait ",
                                    "Landscape",
                                    "Bulb")

    lookups["resolution_units"] = ("",
                                   "Undefined",
                                   "Inches",
                                   "Centimetres")

    lookups["orientations"] = ("",
                               "Horizontal",
                               "Mirror horizontal",
                               "Rotate 180",
                               "Mirror vertical",
                               "Mirror horizontal and rotate 270 CW",
                               "Rotate 90 CW",
                               "Mirror horizontal and rotate 90 CW",
                               "Rotate 270 CW")

    return lookups


def _process_exif_dict(exif_dict):

    date_format = "%Y:%m:%d %H:%M:%S"

    lookups = _create_lookups()

    exif_dict["DateTime"]["processed"] = \
        str(datetime.datetime.strptime(exif_dict["DateTime"]["processed"], date_format))

    exif_dict["DateTimeOriginal"]["processed"] = \
        str(datetime.datetime.strptime(exif_dict["DateTimeOriginal"]["processed"], date_format))

    exif_dict["DateTimeDigitized"]["processed"] = \
        str(datetime.datetime.strptime(exif_dict["DateTimeDigitized"]["processed"], date_format))

    exif_dict["FNumber"]["processed"] = \
        _derationalize(exif_dict["FNumber"]["processed"])
    exif_dict["FNumber"]["processed"] = \
        "f{}".format(exif_dict["FNumber"]["processed"])

    exif_dict["MaxApertureValue"]["processed"] = \
        _derationalize(exif_dict["MaxApertureValue"]["processed"])
    exif_dict["MaxApertureValue"]["processed"] = \
        "f{:2.1f}".format(exif_dict["MaxApertureValue"]["processed"])

    exif_dict["FocalLength"]["processed"] = \
        _derationalize(exif_dict["FocalLength"]["processed"])
    exif_dict["FocalLength"]["processed"] = \
        "{}mm".format(exif_dict["FocalLength"]["processed"])

    exif_dict["FocalLengthIn35mmFilm"]["processed"] = \
        "{}mm".format(exif_dict["FocalLengthIn35mmFilm"]["processed"])

    exif_dict["Orientation"]["processed"] = \
        lookups["orientations"][exif_dict["Orientation"]["processed"]]

    exif_dict["ResolutionUnit"]["processed"] = \
        lookups["resolution_units"][exif_dict["ResolutionUnit"]["processed"]]

    exif_dict["ExposureProgram"]["processed"] = \
        lookups["exposure_programs"][exif_dict["ExposureProgram"]["processed"]]

    exif_dict["MeteringMode"]["processed"] = \
        lookups["metering_modes"][exif_dict["MeteringMode"]["processed"]]

    exif_dict["XResolution"]["processed"] = \
        int(_derationalize(exif_dict["XResolution"]["processed"]))

    exif_dict["YResolution"]["processed"] = \
        int(_derationalize(exif_dict["YResolution"]["processed"]))

    exif_dict["ExposureTime"]["processed"] = \
        _derationalize(exif_dict["ExposureTime"]["processed"])
    exif_dict["ExposureTime"]["processed"] = \
        str(Fraction(exif_dict["ExposureTime"]["processed"]).limit_denominator(8000))

    exif_dict["ExposureBiasValue"]["processed"] = \
        _derationalize(exif_dict["ExposureBiasValue"]["processed"])
    exif_dict["ExposureBiasValue"]["processed"] = \
        "{} EV".format(exif_dict["ExposureBiasValue"]["processed"])
    return exif_dict


def save_gallery_photo(file,profile,name=False):
    if not name:
        path = file_uploader.get_temp_path(file.name,profile)
    else:
        path = file_uploader.get_temp_path(name,profile)
    if (ply.settings.PLY_AVATAR_STORAGE_USE_S3 == 'TRUE'):
        import boto3,io
        client = boto3.client('s3',aws_access_key_id=ply.settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=ply.settings.AWS_SECRET_ACCESS_KEY,endpoint_url=ply.settings.AWS_S3_ENDPOINT_URL)
        try: 
            keystr= f'{ply.settings.PLY_GALLERY_FILE_BASE_PATH}/{path}'
            cache = io.BytesIO()
            file.save(cache,file.format)
            cache.seek(0)
            client.put_object(Body=cache,ACL='public-read', Bucket=ply.settings.AWS_STORAGE_BUCKET_NAME, Key=keystr)
            bw = cache.tell()
            cache.close()
            return bw
        except:
            raise Exception('Unable to store Photo in S3 Storage')
    else:
        destpath = ply.settings.PLY_GALLERY_FILE_BASE_PATH+path
        if not os.path.exists(os.pahgth.dirname(destpath)):
            try:
                os.makedirs(os.path.dirname(destpath))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(destpath, 'wb+') as destination:
            file.save(destination)
            bw = destination.tell()
            destination.close()
            return bw
