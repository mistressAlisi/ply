CREATE OR REPLACE FUNCTION ply_appregistry_updateversion() RETURNS trigger AS $ply_appregistry_updateversion$
DECLARE
    vhist text;

BEGIN
    --- Update indices, first: ---
    IF NEW.updated IS NULL THEN
        INSERT INTO ply_application_version_history (uuid,application_id,new_version_string,old_version_string,updated) VALUES (gen_random_uuid(),NEW.uuid,NEW.version_release||'.'||NEW.version_major||'.'||NEW.version_minor,'0.0.0',now());
    ELSE
        SELECT  new_version_string INTO vhist from ply_application_version_history WHERE application_id = NEW.uuid ORDER BY new_version_string DESC LIMIT 1;
        INSERT INTO ply_application_version_history (uuid,application_id,new_version_string,old_version_string,updated) VALUES (gen_random_uuid(),NEW.uuid,NEW.version_release||'.'||NEW.version_major||'.'||NEW.version_minor,vhist,now());
    END IF;
    RETURN NEW;
END;
$ply_appregistry_updateversion$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "after_insert_updateVersion" ON "ply_application";
CREATE TRIGGER "after_insert_updateVersion" AFTER INSERT ON "ply_application"
FOR EACH ROW EXECUTE FUNCTION ply_appregistry_updateversion();

DROP TRIGGER  IF EXISTS  "after_update_updateVersion" ON "ply_application";
CREATE TRIGGER "after_update_updateVersion" AFTER UPDATE ON "ply_application"
FOR EACH ROW EXECUTE FUNCTION ply_appregistry_updateversion();