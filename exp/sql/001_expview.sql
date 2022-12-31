  DROP VIEW  IF EXISTS "exp_profile_lvlview";
 CREATE OR REPLACE VIEW "exp_profile_lvlview" AS SELECT profiles_profile.uuid,
    profiles_profile.profile_id,
    profiles_profile.created,
    profiles_profile.updated,
    profiles_profile.last_seen,
    profiles_profile.age,
    profiles_profile.name,
    profiles_profile.status,
    profiles_profile.species,
    profiles_profile.introduction,
    profiles_profile.slug,
    profiles_profile.pronouns,
    profiles_profile.gender,
    profiles_profile.avatar,
    profiles_profile.system,
    exp_profileexperience.expr,
    exp_profileexperience.level_id,
    exp_profileexperience.classtype_id,
    exp_profileexperience.community_id,
    stats_classtype.name AS class_name,
    exp_level.level
   FROM profiles_profile
     JOIN exp_profileexperience ON profiles_profile.uuid = exp_profileexperience.profile_id
     JOIN stats_classtype ON exp_profileexperience.classtype_id = stats_classtype.uuid
     JOIN exp_level ON exp_profileexperience.level_id = exp_level.uuid;
