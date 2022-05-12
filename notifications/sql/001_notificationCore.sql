CREATE OR REPLACE FUNCTION notifications_sendToInbox() RETURNS trigger AS $notifications_sendToInbox$
DECLARE
    iterator RECORD;
BEGIN
    --- Update indices, first: ---
    UPDATE profiles_profile SET posts = profiles_profile.posts + 1 WHERE uuid = NEW.source_id;
    UPDATE community_community SET posts = community_community.posts + 1 WHERE uuid = NEW.community_id;
    --- Find all the friends of the source profile, and add the notification to their inbox and their profile: --
    FOR iterator IN 
        SELECT friend1_id,friend2_id FROM community_friend WHERE community_id = NEW.community_id
        LOOP
            IF iterator.friend1_id != NEW.source_id THEN
                INSERT INTO notifications_notificationinbox (notification_id,community_id,recipient_id,created,archived,hidden,system,deleted) VALUES (NEW.uuid,NEW.community_id,iterator.friend1_id,current_timestamp,false,false,false,false) ON CONFLICT DO NOTHING;
                UPDATE profiles_profile SET notifications = profiles_profile.notifications + 1 WHERE uuid = iterator.friend1_id;
            ELSE
                INSERT INTO notifications_notificationinbox (notification_id,community_id,recipient_id,created,archived,hidden,system,deleted) VALUES (NEW.uuid,NEW.community_id,iterator.friend2_id,current_timestamp,false,false,false,false) ON CONFLICT DO NOTHING;
                UPDATE profiles_profile SET notifications = profiles_profile.notifications + 1 WHERE uuid = iterator.friend2_id;
            END IF;
    END LOOP;
    
    --- Find all the followers of the source profile, and add the notification to their inbox and their profile: --
    --  THIS GETS A BIT TRICKY: THE DESTINATION is the profile BEING watched, so we must select the Watching SOURCE! don't get confused. --
    
    FOR iterator IN 
        SELECT source_id FROM community_follower WHERE community_id = NEW.community_id AND dest_id = NEW.source_id
        LOOP
            INSERT INTO notifications_notificationinbox (notification_id,community_id,recipient_id,created,archived,hidden,system,deleted) VALUES (NEW.uuid,NEW.community_id,iterator.source_id,current_timestamp,false,false,false,false)  ON CONFLICT DO NOTHING;
            UPDATE profiles_profile SET notifications = profiles_profile.notifications + 1 WHERE uuid = iterator.source_id;

    END LOOP;
        
    RETURN NEW;
END;
$notifications_sendToInbox$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER TRIGGER_sendNotifications_AfterINST AFTER INSERT ON "notifications_notification"
FOR EACH ROW EXECUTE FUNCTION notifications_sendToInbox();
