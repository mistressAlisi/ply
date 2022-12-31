DROP VIEW IF EXISTS "community_profilepercommunityview";
CREATE OR REPLACE VIEW "community_profilepercommunityview" AS  SELECT DISTINCT
community_communityprofile.community_id, 
community_community.created AS joined, 
community_community."name" AS community_name, 
community_community.uuid AS community_uuid,
profiles_profile.uuid, 
profiles_profile.profile_id, 
profiles_profile.created AS profile_created, 
profiles_profile.updated AS profile_updated, 
profiles_profile.creator_id AS profile_creator,
profiles_profile.last_seen, 
profiles_profile.age, 
profiles_profile."name",
profiles_profile.status, 
profiles_profile.species, 
profiles_profile.introduction, 
profiles_profile."level", 
profiles_profile."max_HP", 
profiles_profile."HP", 
profiles_profile."max_MP", 
profiles_profile."max_STUN", 
profiles_profile."STUN", 
profiles_profile."SHIELD", 
profiles_profile."MP", 
profiles_profile."max_SHIELD", 
profiles_profile."max_STA", 
profiles_profile.slug, 
profiles_profile.pronouns, 
profiles_profile."STA", 
profiles_profile.avatar, 
profiles_profile.gender, 
profiles_profile.posts, 
profiles_profile.views, 
profiles_profile.nodes, 
profiles_profile.archived, 
profiles_profile.blocked, 
profiles_profile.frozen, 
profiles_profile."system", 
profiles_profile.creator_id, 
profiles_profile.dynapage_id
FROM
community_communityprofile
INNER JOIN
community_community
ON 
community_communityprofile.community_id = community_community.uuid
INNER JOIN
profiles_profile
ON 
community_communityprofile.profile_id = profiles_profile.uuid
WHERE
profiles_profile.placeholder = false;

DROP VIEW IF EXISTS "community_friend_explvl_view";
CREATE VIEW "community_friend_explvl_view" AS SELECT
    community_friend.id as id,
	community_friend.friend1_id,
	community_friend.friend2_id,
	community_friend.community_id,
	exp_profile_lvlview.profile_id,
	exp_profile_lvlview.created,
	exp_profile_lvlview.updated,
	exp_profile_lvlview.last_seen,
	exp_profile_lvlview.age,
	exp_profile_lvlview."name",
	exp_profile_lvlview.status,
	exp_profile_lvlview.species,
	exp_profile_lvlview.introduction,
	exp_profile_lvlview.pronouns,
	exp_profile_lvlview.slug,
	exp_profile_lvlview.gender,
	exp_profile_lvlview.avatar,
	exp_profile_lvlview."system",
	exp_profile_lvlview.level_id,
	exp_profile_lvlview.classtype_id,
	exp_profile_lvlview.class_name,
	exp_profile_lvlview.expr,
	exp_profile_lvlview."level" AS current_level,
	community_friend.approved,
	community_friend.approved_flag
FROM
	exp_profile_lvlview
	JOIN
	community_friend
	ON
		exp_profile_lvlview.uuid = community_friend.friend2_id;


DROP VIEW IF EXISTS "community_friend2_explvl_view";
CREATE VIEW "community_friend2_explvl_view" AS SELECT
    community_friend.id as id,
	community_friend.friend1_id,
	community_friend.friend2_id,
	community_friend.community_id,
	exp_profile_lvlview.profile_id,
	exp_profile_lvlview.created,
	exp_profile_lvlview.updated,
	exp_profile_lvlview.last_seen,
	exp_profile_lvlview.age,
	exp_profile_lvlview."name",
	exp_profile_lvlview.status,
	exp_profile_lvlview.species,
	exp_profile_lvlview.introduction,
	exp_profile_lvlview.pronouns,
	exp_profile_lvlview.slug,
	exp_profile_lvlview.gender,
	exp_profile_lvlview.avatar,
	exp_profile_lvlview."system",
	exp_profile_lvlview.level_id,
	exp_profile_lvlview.classtype_id,
	exp_profile_lvlview.class_name,
	exp_profile_lvlview.expr,
	exp_profile_lvlview."level" AS current_level,
	community_friend.approved,
	community_friend.approved_flag
FROM
	exp_profile_lvlview
	JOIN
	community_friend
	ON
		exp_profile_lvlview.uuid = community_friend.friend2_id;
