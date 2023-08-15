CREATE OR REPLACE FUNCTION gallery_gc_upcount() RETURNS trigger AS $gallery_gc_upcount$
BEGIN
    --- Update indices, first: ---
    UPDATE media_gallery_core_collection SET items = media_gallery_core_collection.items + 1 WHERE uuid = NEW.collection_id;
    RETURN NEW;
END;
$gallery_gc_upcount$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "after_Inst_ColCounter" ON "media_gallery_core_collection_items";
CREATE TRIGGER "after_Inst_ColCounter" AFTER INSERT ON "media_gallery_core_collection_items"
FOR EACH ROW EXECUTE FUNCTION gallery_gc_upcount();



CREATE OR REPLACE FUNCTION gallery_gc_dccount() RETURNS trigger AS $gallery_gc_dccount$
BEGIN
    --- Update indices, first: ---
    UPDATE media_gallery_core_collection SET items = media_gallery_core_collection.items - 1 WHERE uuid = OLD.collection_id;
    RETURN OLD;
END;
$gallery_gc_dccount$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "after_Del_ColCounter" ON "media_gallery_core_collection_items";
CREATE TRIGGER "after_Del_ColCounter" AFTER DELETE ON "media_gallery_core_collection_items"
FOR EACH ROW EXECUTE FUNCTION gallery_gc_dccount();
