import ply
class gallery_upload_plugin():
    content_type_info = {
        "label":"Photos",
        "id":"photos",
        "icon":"fas fa-photo-video",
        "desc":"The Photography core is ideal for uploading all types of Photographic content from Cameras and Smartphones alike.",
        "upload_form":"gallery_photos_upload_form.html",
        "review_form":"gallery_photos_review_form.html",
        },
    content_accept_filetypes = [
        "jpeg",
        "jpg",
        "png",
        "tif",
        "tiff"
        ],
    content_accept_filetypes_str = ",".join(map(str, content_accept_filetypes)) 

    content_max_file_size_kb = ply.settings.PLY_GALLERY_MAX_ORIGINAL_SIZE
