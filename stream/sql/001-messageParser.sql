CREATE OR REPLACE FUNCTION stream_parseMessage() RETURNS trigger AS $stream_parseMessage$
DECLARE
    STREAM stream_stream%rowtype;
    MSG text;
BEGIN
    --- Get Data: ---
    SELECT * INTO STREAM from stream_stream WHERE uuid = NEW.stream_id;
    ---RAISE NOTICE 'UUID: %',NEW.stream_id;---
    --- PARSE the message: ---
    IF ((NEW.type = 'text/plain') AND (NEW.contents_text IS NOT NULL)) THEN
    MSG  := keywords_parsestr(NEW.contents_text);
    MSG  := profiles_parsestr_and_mention(MSG,'stream.message',CAST(NEW.uuid as text),STREAM.community_id);
    ---RAISE NOTICE 'Message is %',MSG;---
    ---UPDATE "stream_streammessage" SET contents_text_parsed = MSG where uuid = NEW.uuid;---
        NEW.contents_text_parsed = MSG;
    END IF;
    RETURN NEW;
END;
$stream_parseMessage$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER "stream_parseMessage" BEFORE INSERT ON "stream_streammessage"
FOR EACH ROW EXECUTE FUNCTION stream_parseMessage();
