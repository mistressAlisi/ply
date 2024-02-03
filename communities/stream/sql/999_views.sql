DROP VIEW IF EXISTS  communities_stream_message_view;
CREATE OR REPLACE VIEW communities_stream_message_view  AS SELECT DISTINCT
	communities_stream_stream_message.uuid AS id,
	communities_stream_stream.community_id AS community_id,
	communities_stream_stream.uuid AS stream_id,
	communities_stream_stream.created AS stream_created,
	communities_stream_stream."type" AS stream_type,
	communities_stream_stream.icon AS stream_icon,
	communities_stream_stream.shares AS stream_shares,
	communities_stream_stream.views AS stream_views,
	communities_stream_stream.nodes AS stream_nodes,
	communities_stream_stream.archived AS stream_archived,
	communities_stream_stream.hidden AS stream_hidden,
	communities_stream_stream."system" AS stream_system,
	communities_stream_stream.group_id AS stream_group_id,
	communities_stream_stream.profile_id AS stream_profile_id,
	profiles.uuid AS profile_uuid,
	profiles.profile_id AS profile_id,
	profiles.created AS profile_created,
	profiles.updated AS profile_updated,
	profiles.last_seen AS profile_last_seen,
	profiles.age AS profile_age,
	profiles."name" AS profile_name,
	profiles.status AS profile_status,
	profiles.species AS profile_species,
	profiles.introduction AS profile_introduction,
	profiles.pronouns AS profile_pronouns,
	profiles.gender AS profile_gender,
	profiles.avatar AS profile_avatar,
	profiles.posts AS profile_posts,
	profiles.views AS profile_views,
	profiles.nodes AS profile_nodes,
	profiles.archived AS profile_archieved,
	profiles.frozen AS profile_frozen,
	profiles."system" AS profile_system,
	profiles.blocked AS profile_blocked,
	communities_stream_stream_message.uuid AS message_uuid,
	communities_stream_stream_message.author_id AS author_id,
	communities_stream_stream_message.created AS message_created,
	communities_stream_stream_message."type" AS message_type,
	communities_stream_stream_message.icon AS message_icon,
	communities_stream_stream_message.shares AS shares,
	communities_stream_stream_message.views AS views,
	communities_stream_stream_message.contents_text AS contents_text,
	communities_stream_stream_message.contents_json AS contents_json,
	communities_stream_stream_message.contents_bin AS contents_bin,
	communities_stream_stream_message.likes AS likes,
	communities_stream_stream_message.reposts AS reposts,
	communities_stream_stream_message.threads AS threads,
	communities_stream_stream_message.replies AS replies,
	communities_stream_stream_message.contents_text_parsed AS contents_text_parsed,
	communities_stream_stream_message.references_id AS references_id
FROM
	communities_stream_stream
	FULL OUTER JOIN
	communities_stream_stream_message
	ON
		communities_stream_stream.uuid = communities_stream_stream_message.posted_in_id OR
		communities_stream_stream.uuid = communities_stream_stream_message.stream_id
	INNER JOIN
	communities_profiles_profile AS profiles
	ON
		communities_stream_stream.profile_id = profiles.uuid;


