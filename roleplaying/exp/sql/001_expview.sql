-- DROP VIEW  IF EXISTS "roleplaying_exp_profile_lvlview";
 CREATE OR REPLACE VIEW "roleplaying_exp_profile_lvlview" AS SELECT communities_profiles_profile.uuid,
    communities_profiles_profile.profile_id,
    communities_profiles_profile.created,
    communities_profiles_profile.updated,
    communities_profiles_profile.last_seen,
    communities_profiles_profile.age,
    communities_profiles_profile.name,
    communities_profiles_profile.status,
    communities_profiles_profile.species,
    communities_profiles_profile.introduction,
    communities_profiles_profile.slug,
    communities_profiles_profile.pronouns,
    communities_profiles_profile.gender,
    communities_profiles_profile.avatar,
    communities_profiles_profile.system,
    roleplaying_exp_profile_experience.expr,
    roleplaying_exp_profile_experience.level_id,
    roleplaying_exp_profile_experience.classtype_id,
    roleplaying_exp_profile_experience.community_id,
    roleplaying_stats_class_type.name AS class_name,
    roleplaying_exp_level.level
   FROM communities_profiles_profile
     JOIN roleplaying_exp_profile_experience ON communities_profiles_profile.uuid = roleplaying_exp_profile_experience.profile_id
     JOIN roleplaying_stats_class_type ON roleplaying_exp_profile_experience.classtype_id = roleplaying_stats_class_type.uuid
     JOIN roleplaying_exp_level ON roleplaying_exp_profile_experience.level_id = roleplaying_exp_level.uuid;




-- DROP VIEW IF EXISTS "communities_community_friend_explvl_view";
CREATE OR REPLACE VIEW "communities_community_friend_explvl_view" AS SELECT
    communities_community_friend.id as id,
	communities_community_friend.friend1_id,
	communities_community_friend.friend2_id,
	communities_community_friend.community_id,
	roleplaying_exp_profile_lvlview.profile_id,
	roleplaying_exp_profile_lvlview.created,
	roleplaying_exp_profile_lvlview.updated,
	roleplaying_exp_profile_lvlview.last_seen,
	roleplaying_exp_profile_lvlview.age,
	roleplaying_exp_profile_lvlview."name",
	roleplaying_exp_profile_lvlview.status,
	roleplaying_exp_profile_lvlview.species,
	roleplaying_exp_profile_lvlview.introduction,
	roleplaying_exp_profile_lvlview.pronouns,
	roleplaying_exp_profile_lvlview.slug,
	roleplaying_exp_profile_lvlview.gender,
	roleplaying_exp_profile_lvlview.avatar,
	roleplaying_exp_profile_lvlview."system",
	roleplaying_exp_profile_lvlview.level_id,
	roleplaying_exp_profile_lvlview.classtype_id,
	roleplaying_exp_profile_lvlview.class_name,
	roleplaying_exp_profile_lvlview.expr,
	roleplaying_exp_profile_lvlview."level" AS current_level,
	communities_community_friend.approved,
	communities_community_friend.approved_flag
FROM
	roleplaying_exp_profile_lvlview
	JOIN
	communities_community_friend
	ON
		roleplaying_exp_profile_lvlview.uuid = communities_community_friend.friend2_id;


DROP VIEW IF EXISTS "communities_community_friend2_explvl_view";
CREATE VIEW "communities_community_friend2_explvl_view" AS SELECT
    communities_community_friend.id as id,
	communities_community_friend.friend1_id,
	communities_community_friend.friend2_id,
	communities_community_friend.community_id,
	roleplaying_exp_profile_lvlview.profile_id,
	roleplaying_exp_profile_lvlview.created,
	roleplaying_exp_profile_lvlview.updated,
	roleplaying_exp_profile_lvlview.last_seen,
	roleplaying_exp_profile_lvlview.age,
	roleplaying_exp_profile_lvlview."name",
	roleplaying_exp_profile_lvlview.status,
	roleplaying_exp_profile_lvlview.species,
	roleplaying_exp_profile_lvlview.introduction,
	roleplaying_exp_profile_lvlview.pronouns,
	roleplaying_exp_profile_lvlview.slug,
	roleplaying_exp_profile_lvlview.gender,
	roleplaying_exp_profile_lvlview.avatar,
	roleplaying_exp_profile_lvlview."system",
	roleplaying_exp_profile_lvlview.level_id,
	roleplaying_exp_profile_lvlview.classtype_id,
	roleplaying_exp_profile_lvlview.class_name,
	roleplaying_exp_profile_lvlview.expr,
	roleplaying_exp_profile_lvlview."level" AS current_level,
	communities_community_friend.approved,
	communities_community_friend.approved_flag
FROM
	roleplaying_exp_profile_lvlview
	JOIN
	communities_community_friend
	ON
		roleplaying_exp_profile_lvlview.uuid = communities_community_friend.friend2_id;
