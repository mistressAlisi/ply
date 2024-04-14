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

CREATE OR REPLACE FUNCTION gallery_install_plugin_hist() RETURNS trigger as $gallery_install_plugin_hist$
DECLARE
    current_install media_gallery_core_plugins%ROWTYPE;
BEGIN
    IF EXISTS (SELECT id FROM media_gallery_core_plugins WHERE id=NEW.id) THEN
        SELECT * into current_install from media_gallery_core_plugins WHERE id=NEW.id;
        INSERT INTO media_gallery_core_plugin_version_history (old_version,version,updated,app_id) VALUES (current_install.version,NEW.version,current_timestamp,NEW.id);
    ELSE
        INSERT INTO media_gallery_core_plugin_version_history (old_version,version,updated,app_id) VALUES ('0.0.0,0',NEW.version,current_timestamp,NEW.id);
    END IF;

RETURN NEW;
END;
$gallery_install_plugin_hist$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "before_update_on_galversion" ON "media_gallery_core_plugins";
DROP TRIGGER IF EXISTS "after_insert_on_galversion" ON "media_gallery_core_plugins";
CREATE TRIGGER "before_update_on_galversion" BEFORE UPDATE ON "media_gallery_core_plugins"
FOR EACH ROW EXECUTE FUNCTION gallery_install_plugin_hist();
CREATE TRIGGER "after_insert_on_galversion" AFTER INSERT ON "media_gallery_core_plugins"
FOR EACH ROW EXECUTE FUNCTION gallery_install_plugin_hist();