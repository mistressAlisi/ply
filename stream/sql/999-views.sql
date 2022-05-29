DROP VIEW IF EXISTS  stream_messageview;
CREATE OR REPLACE VIEW stream_messageview  AS SELECT DISTINCT
	stream_streammessage.uuid AS id,
	stream_stream.community_id AS community_id,
	stream_stream.uuid AS stream_id,
	stream_stream.created AS stream_created,
	stream_stream."type" AS stream_type,
	stream_stream.icon AS stream_icon,
	stream_stream.shares AS stream_shares,
	stream_stream.views AS stream_views,
	stream_stream.nodes AS stream_nodes,
	stream_stream.archived AS stream_archived,
	stream_stream.hidden AS stream_hidden,
	stream_stream."system" AS stream_system,
	stream_stream.group_id AS stream_group_id,
	stream_stream.profile_id AS stream_profile_id,
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
	stream_streammessage.uuid AS message_uuid,
	stream_streammessage.author_id AS author_id,
	stream_streammessage.created AS message_created,
	stream_streammessage."type" AS message_type,
	stream_streammessage.icon AS message_icon,
	stream_streammessage.shares AS shares,
	stream_streammessage.views AS views,
	stream_streammessage.contents_text AS contents_text,
	stream_streammessage.contents_json AS contents_json,
	stream_streammessage.contents_bin AS contents_bin,
	stream_streammessage.likes AS likes,
	stream_streammessage.reposts AS reposts,
	stream_streammessage.threads AS threads,
	stream_streammessage.replies AS replies,
	stream_streammessage.contents_text_parsed AS contents_text_parsed,
	stream_streammessage.references_id AS references_id
FROM
	stream_stream
	FULL OUTER JOIN
	stream_streammessage
	ON
		stream_stream.uuid = stream_streammessage.posted_in_id OR
		stream_stream.uuid = stream_streammessage.stream_id
	INNER JOIN
	profiles_profile AS profiles
	ON
		stream_stream.profile_id = profiles.uuid;


