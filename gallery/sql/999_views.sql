DROP VIEW IF EXISTS "gallery_itemsbycollectionpermission";
CREATE OR REPLACE VIEW "gallery_itemsbycollectionpermission" AS  SELECT DISTINCT
    gallery_gallerycollectionpermission.id AS gcp_id,
    gallery_gallerycollectionpermission.updated AS gcp_updated,
    gallery_gallerycollectionpermission.owner AS gcp_owner,
    gallery_gallerycollectionpermission.archived AS gcp_archived,
    gallery_gallerycollectionpermission.public AS gcp_public,
    gallery_gallerycollectionpermission.searchable AS gcp_searchable,
    gallery_gallerycollectionpermission.shareable AS gcp_shareable,
    gallery_gallerycollectionpermission."create" AS gcp_create,
    gallery_gallerycollectionpermission.edit AS gcp_edit,
    gallery_gallerycollectionpermission.delete AS gcp_delete,
    gallery_gallerycollectionpermission.nsfw AS gcp_nsfw,
    gallery_gallerycollectionpermission.explicit AS gcp_explicit,
    gallery_gallerycollectionpermission.comment AS gcp_comment,
    gallery_gallerycollectionpermission.profile_id AS gcp_profile,
    gallery_gallerycollectionpermission.community_id AS gcp_community,
    gallery_gallerycollection.collection_id AS gc_id,
    gallery_gallerycollection.label AS gc_label,
    gallery_gallerycollection.created AS gc_created,
    gallery_gallerycollection.updated AS gc_updated,
    gallery_gallerycollection.items AS gc_items,
    gallery_gallerycollection.views AS gc_views,
    gallery_gallerycollection.likes AS gc_likes,
    gallery_gallerycollection.shares AS gc_shares,
    gallery_gallerycollection.comments AS gc_comments,
    gallery_gallerycollection.uuid AS gc_uuid,
    gallery_gallerycollectionitems."order" AS gci_order,
    gallery_galleryitem.item_hash AS gci_hash,
    gallery_galleryitem.title AS gci_title,
    gallery_galleryitem.descr AS gci_descr,
    gallery_galleryitem.created AS gci_created,
    gallery_galleryitem.updated AS gci_updated,
    gallery_galleryitem.files AS gci_files,
    gallery_galleryitem.views AS gci_views,
    gallery_galleryitem.likes AS gci_likes,
    gallery_galleryitem.shares AS gci_shares,
    gallery_galleryitem.comments AS gci_comments,
    gallery_galleryitem.nsfw AS gci_nsfw,
    gallery_galleryitem.plugin AS gci_plugin,
    gallery_galleryitem.plugin_data AS gci_plugin_data,
    gallery_galleryitem.thumbnail AS gci_thumbnail,
    gallery_galleryitem.processed AS gci_processed,
    gallery_galleryitem.uuid AS gci_uuid,
    gallery_galleryitem.configured AS gci_configured,
    gallery_galleryitem.active AS gci_active,
    gallery_galleryitem.archived AS gci_archived,
    gallery_galleryitem.frozen AS gci_frozen,
    gallery_galleryitem.hidden AS gci_hidden,
    gallery_galleryitem.downloads AS gci_downloads,
    gallery_galleryitem.profile_id AS gci_profile,
    gallery_galleryitem.details AS gci_details,
    gallery_galleryitem.sizing AS gci_sizing,
    gallery_galleryitem.style AS gci_style,
    gallery_galleryitem.rating AS gci_rating,
    gallery_galleryitemfile.name AS gif_name,
    gallery_galleryitemfile.hash AS gif_hash,
    gallery_galleryitemfile.id AS gif_id,
    gallery_galleryitemfile.data AS gif_data,
    gallery_galleryitemfile.created AS gif_created,
    gallery_galleryitemfile.updated AS gif_updated,
    gallery_galleryitemfile.meta AS gif_meta,
    gallery_galleryitemfile.bindata AS gif_bindata,
    gallery_galleryitemfile.jsondata AS gif_jsondata,
    gallery_galleryitemfile.thumbnail AS gif_thumbnail,
    gallery_galleryitemfile.file_size AS gif_size,
    gallery_galleryitemfile.type AS gif_type,
    gallery_galleryitemfile.original AS gif_original,
    gallery_galleryitemfile.item_id AS gif_item,
    gallery_gallerycollectionpermission.id AS id,
    gallery_gallerycollection.uuid AS collection_id,
    gallery_gallerycollectionpermission.community_id AS community_id,
    gallery_galleryitemfile.id as file_id,
    gallery_galleryitem.uuid as item_id,
    profiles_profile.name as profile_name,
    profiles_profile.pronouns as profile_pronouns,
    profiles_profile.avatar as profile_avatar,
    profiles_profile.slug as profile_slug,
    profiles_profile.uuid as profile_uuid,
    profiles_profile.uuid as profile_id
   FROM gallery_gallerycollectionpermission
     JOIN gallery_gallerycollection ON gallery_gallerycollectionpermission.collection_id = gallery_gallerycollection.uuid
     JOIN gallery_gallerycollectionitems ON gallery_gallerycollection.uuid = gallery_gallerycollectionitems.collection_id
     JOIN gallery_galleryitem ON gallery_gallerycollectionitems.item_id = gallery_galleryitem.uuid
     JOIN gallery_galleryitemfile ON gallery_galleryitem.uuid = gallery_galleryitemfile.item_id
     JOIN profiles_profile ON profiles_profile.uuid = gallery_gallerycollectionpermission.profile_id
   WHERE gallery_galleryitemfile.name != ''
   ORDER BY gif_created DESC;  
   
CREATE RULE delete_rule_gallery_itemsbycollectionpermission
AS ON DELETE TO "gallery_itemsbycollectionpermission"
DO INSTEAD NOTHING;
