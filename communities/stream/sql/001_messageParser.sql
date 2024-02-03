CREATE OR REPLACE FUNCTION communities_stream_parseMessage() RETURNS trigger AS $stream_parseMessage$
DECLARE
    STREAM communities_stream_stream%rowtype;
    KEYWORD_IDS int[];
    kw int;
    MSG text;
BEGIN
    --- Get Data: ---
    SELECT * INTO STREAM from communities_stream_stream WHERE uuid = NEW.stream_id;
    ---RAISE NOTICE 'UUID: %',NEW.stream_id;---
    --- PARSE the message: ---
    IF (NEW.contents_text IS NOT NULL) THEN
    MSG  := content_manager_keywords_parsestr(NEW.contents_text);
    MSG  := communities_profiles_parsestr_and_mention(MSG,'stream.message',CAST(NEW.uuid as text),STREAM.community_id);
    --- CREATE KEYWORD links for parsed messag if applicable: ---
    KEYWORD_IDS = content_manager_get_str_keyword_ids(NEW.contents_text);
    if (KEYWORD_IDS IS NOT NULL) THEN
        FOREACH kw in ARRAY KEYWORD_IDS LOOP
            INSERT INTO communities_stream_stream_message_keywords (stream_id,message_id,keyword_id) VALUES (NEW.stream_id,NEW.uuid,kw);
        END LOOP;
    END IF;
    ---RAISE NOTICE 'Message is %',MSG;---
    ---UPDATE "communities_stream_streammessage" SET contents_text_parsed = MSG where uuid = NEW.uuid;---
        NEW.contents_text_parsed = MSG;
    END IF;
    RETURN NEW;
END;
$stream_parseMessage$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "stream_parseMessage" ON "communities_stream_stream_message";
CREATE TRIGGER "stream_parseMessage" BEFORE INSERT ON "communities_stream_stream_message"
FOR EACH ROW EXECUTE FUNCTION communities_stream_parseMessage();
