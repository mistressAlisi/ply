CREATE OR REPLACE FUNCTION gallery_gc_upcount() RETURNS trigger AS $gallery_gc_upcount$
BEGIN
    --- Update indices, first: ---
    UPDATE gallery_gallerycollection SET items = gallery_gallerycollection.items + 1 WHERE uuid = NEW.collection_id;
    RETURN NEW;
END;
$gallery_gc_upcount$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "after_Inst_ColCounter" ON "gallery_gallerycollectionitems";
CREATE TRIGGER "after_Inst_ColCounter" AFTER INSERT ON "gallery_gallerycollectionitems"
FOR EACH ROW EXECUTE FUNCTION gallery_gc_upcount();



CREATE OR REPLACE FUNCTION gallery_gc_dccount() RETURNS trigger AS $gallery_gc_dccount$
BEGIN
    --- Update indices, first: ---
    UPDATE gallery_gallerycollection SET items = gallery_gallerycollection.items - 1 WHERE uuid = OLD.collection_id;
    RETURN OLD;
END;
$gallery_gc_dccount$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "after_Del_ColCounter" ON "gallery_gallerycollectionitems";
CREATE TRIGGER "after_Del_ColCounter" AFTER DELETE ON "gallery_gallerycollectionitems"
FOR EACH ROW EXECUTE FUNCTION gallery_gc_dccount();
