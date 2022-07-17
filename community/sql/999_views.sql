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


