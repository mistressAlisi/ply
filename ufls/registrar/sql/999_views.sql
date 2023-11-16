DROP VIEW IF EXISTS ufls_registrar_level_loot_view;
CREATE OR REPLACE VIEW ufls_registrar_level_loot_view AS  SELECT DISTINCT
    ufls_registrar_registrant_level.uuid as id,
	ufls_registrar_registrant_level.uuid as level_id,
	ufls_registrar_registrant_level.level_id as levelid,
	ufls_registrar_registrant_level.label,
	ufls_registrar_registrant_level.active,
	ufls_registrar_registration_loot.label AS loot_label,
	ufls_registrar_registration_loot.active AS loot_active,
	ufls_registrar_registration_loot."cost",
	ufls_registrar_registration_loot.purchasable,
	ufls_registrar_registration_loot.descr,
	ufls_registrar_registration_loot.picture,
	ufls_registrar_registration_loot.id as loot_id,
	ufls_registrar_registration_level_loot.id as level_loot_id


FROM
	ufls_registrar_registrant_level
	INNER JOIN
	ufls_registrar_registration_level_loot
	ON
		ufls_registrar_registrant_level."uuid" = ufls_registrar_registration_level_loot.level_id
	INNER JOIN
	ufls_registrar_registration_loot
	ON
		ufls_registrar_registration_level_loot.item_id = ufls_registrar_registration_loot."id";