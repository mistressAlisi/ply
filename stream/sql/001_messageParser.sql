CREATE OR REPLACE FUNCTION stream_parseMessage() RETURNS trigger AS $stream_parseMessage$
DECLARE
    STREAM stream_stream%rowtype;
    KEYWORD_IDS int[];
    kw int;
    MSG text;
BEGIN
    --- Get Data: ---
    SELECT * INTO STREAM from stream_stream WHERE uuid = NEW.stream_id;
    ---RAISE NOTICE 'UUID: %',NEW.stream_id;---
    --- PARSE the message: ---
    IF (NEW.contents_text IS NOT NULL) THEN
    MSG  := keywords_parsestr(NEW.contents_text);
    MSG  := profiles_parsestr_and_mention(MSG,'stream.message',CAST(NEW.uuid as text),STREAM.community_id);
    --- CREATE KEYWORD links for parsed messag if applicable: ---
    KEYWORD_IDS = get_str_keyword_ids(NEW.contents_text);
    if (KEYWORD_IDS IS NOT NULL) THEN
        FOREACH kw in ARRAY KEYWORD_IDS LOOP
            INSERT INTO stream_streammessagekeywords (stream_id,message_id,keyword_id) VALUES (NEW.stream_id,NEW.uuid,kw);
        END LOOP;
    END IF;
    ---RAISE NOTICE 'Message is %',MSG;---
    ---UPDATE "stream_streammessage" SET contents_text_parsed = MSG where uuid = NEW.uuid;---
        NEW.contents_text_parsed = MSG;
    END IF;
    RETURN NEW;
END;
$stream_parseMessage$ LANGUAGE plpgsql;

DROP TRIGGER  IF EXISTS  "stream_parseMessage" ON "stream_streammessage";
CREATE TRIGGER "stream_parseMessage" BEFORE INSERT ON "stream_streammessage"
FOR EACH ROW EXECUTE FUNCTION stream_parseMessage();
