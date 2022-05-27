CREATE OR REPLACE FUNCTION profiles_parsestr(INPUT_STR text) RETURNS text AS $profiles_parsestr$
DECLARE
    PROFILE profiles_profile%rowtype;
    MESSAGE_STRING text[];
    OUTPUT_STR text;
    MSG text;
    SLUGGED text;
    POSMARK int;
    MSGCOUNT int;
BEGIN
    MESSAGE_STRING := string_to_array(INPUT_STR,' ');
    MSGCOUNT = 1;
    FOREACH MSG IN ARRAY MESSAGE_STRING
  LOOP
   POSMARK := position('@' in MSG);
   IF POSMARK = 1 THEN
        SLUGGED := right(MSG,-1);
        RAISE NOTICE 'Slugged FOR PROFILE! %,',SLUGGED;
        SELECT * INTO PROFILE FROM profiles_profile WHERE  lower(profile_id) =  lower(SLUGGED);
        IF FOUND THEN
            ---INSERT INTO profiles_profile (hash,keyword,created,updated,items,views,likes,dislikes,shares,comments,active,archived,hidden) VALUES (SLUGGED,MSG,current_timestamp,current_timestamp,0,0,0,0,0,0,true,false,false);
            ---SELECT * INTO KEYWORD FROM profiles_profile WHERE hash = SLUGGED;
            MESSAGE_STRING[MSGCOUNT] := '<a class="link pill profile" target="_blank" href="/p/@'||PROFILE.profile_id||'">@'||PROFILE.profile_id||'</a>';
        END IF;
        ---UPDATE profiles_profile SET items = items + 1, UPDATED = current_timestamp WHERE id = KEYWORD.id;
        ---MESSAGE_STRING[MSGCOUNT] := '<a class="link pill keyword" target="_blank" href="/s/k/#'||SLUGGED||'">'||MSG||'</a>';
   END IF;
   MSGCOUNT := MSGCOUNT +1;
  END LOOP;
    OUTPUT_STR := array_to_string(MESSAGE_STRING,' ');
    RETURN OUTPUT_STR;
END;
$profiles_parsestr$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION profiles_parsestr_and_mention(INPUT_STR text,NOTIFY_TYPE text, NOTIFY_DATA text, COMMUNITY uuid) RETURNS text AS $profiles_parsestr_and_mention$
DECLARE
    PROFILE profiles_profile%rowtype;
    MESSAGE_STRING text[];
    OUTPUT_STR text;
    MSG text;
    SLUGGED text;
    POSMARK int;
    MSGCOUNT int;
BEGIN
    MESSAGE_STRING := string_to_array(INPUT_STR,' ');
    MSGCOUNT = 1;
    FOREACH MSG IN ARRAY MESSAGE_STRING
  LOOP
   POSMARK := position('@' in MSG);
   IF POSMARK = 1 THEN
        SLUGGED := right(MSG,-1);
        SELECT * INTO PROFILE FROM profiles_profile WHERE  lower(profile_id) =  lower(SLUGGED);
        IF FOUND THEN
            INSERT INTO notifications_mentions (created,archived,hidden,system,type,contents_text,recipient_id,community_id) VALUES (current_timestamp,false,false,false,$2,$3,PROFILE.uuid,$4);
            MESSAGE_STRING[MSGCOUNT] := '<a class="link pill profile" target="_blank" href="/p/@'||PROFILE.profile_id||'">@'||PROFILE.profile_id||'</a>';
        END IF;
        ---UPDATE profiles_profile SET items = items + 1, UPDATED = current_timestamp WHERE id = KEYWORD.id;
        ---MESSAGE_STRING[MSGCOUNT] := '<a class="link pill keyword" target="_blank" href="/s/k/#'||SLUGGED||'">'||MSG||'</a>';
   END IF;
   MSGCOUNT := MSGCOUNT +1;
  END LOOP;
    OUTPUT_STR := array_to_string(MESSAGE_STRING,' ');
    RETURN OUTPUT_STR;
END;
$profiles_parsestr_and_mention$ LANGUAGE plpgsql;







