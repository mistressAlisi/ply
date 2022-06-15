from django.urls import path,include
from gallery import api_views

urlpatterns = [
    path('upload/get_categories',api_views.get_categories),
    path('upload/get_collections/w+',api_views.get_collections_writeable),
    path('upload/get_form/<plugin>',api_views.get_form),
    path('upload/post_upload_thumbs/',api_views.post_upload_thumbs),
    path('upload/post_upload/',api_views.post_upload),
    path('upload/review_panel/<file_id>',api_views.get_review_panel),
    path('upload/publish/<file_id>',api_views.publish_after_review),
    path('get/all_collections/',api_views.gallery_collections_raw),
    path('get/items/<collection>',api_views.gallery_collection_items_raw),
    path('view_counter/item/',api_views.gallery_viewer_counter_item),
    path('share_counter/item/',api_views.gallery_share_counter_item),
    path('recast/<uuid:col>/<uuid:item>',api_views.gallery_recast_item),
    path('toggle/invis/<uuid:item>',api_views.gallery_toggle_invisible),
    path('remove/temp/<int:item>',api_views.gallery_remove_temp),
    path('remove/item/form/<uuid:item>/<uuid:col>',api_views.gallery_remitem_form),
    path('remove/item/form/exec',api_views.gallery_remove_exec),
    path('copymove/form/<uuid:item>/<uuid:col>',api_views.gallery_copymove_form),
    path('copymove/form/exec',api_views.gallery_copymove_exec),
    path('settings/item/form/<uuid:item>/<uuid:col>',api_views.gallery_settings_form),
    path('settings/item/form/exec',api_views.gallery_update_settings),
    path('metadata/item/<uuid:item>/<uuid:col>',api_views.gallery_item_metadata),
    path('details/item/form/<uuid:item>/<uuid:col>',api_views.gallery_details_form),
    path('details/item/form/exec',api_views.gallery_update_details),
]
