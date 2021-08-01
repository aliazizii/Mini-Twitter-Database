DELIMITER //

CREATE TRIGGER auto_like
AFTER INSERT
ON likes FOR EACH ROW
    BEGIN
        DECLARE id INT;
        SET id = NEW.tweetid;
        UPDATE tweet SET likes = likes + 1 WHERE tweetid = id;
    END //


CREATE TRIGGER auto_follow
BEFORE INSERT
ON follow FOR EACH ROW
    BEGIN
        DECLARE follower_temp VARCHAR(20);
        DECLARE following_temp VARCHAR(20);
        SET follower_temp = NEW.follower;
        SET following_temp = NEW.following;
        UPDATE users SET following = users.following + 1 WHERE username = follower_temp;
        UPDATE users SET followers = followers + 1 WHERE username = following_temp;
    end //


CREATE TRIGGER auto_stop_follow
BEFORE DELETE
ON follow FOR EACH ROW
    BEGIN
        DECLARE follower_temp VARCHAR(20);
        DECLARE following_temp VARCHAR(20);
        SET follower_temp = OLD.follower;
        SET following_temp = OLD.following;
        UPDATE users SET following = users.following - 1 WHERE username = follower_temp;
        UPDATE users SET followers = followers - 1 WHERE username = following_temp;
    end //


CREATE TRIGGER auto_login
AFTER INSERT
ON users FOR EACH ROW
    BEGIN
        INSERT INTO login_record(USERNAME, TIMESTAMP_T) VALUES (NEW.username, CURRENT_TIMESTAMP);
    end //


CREATE TRIGGER auto_add_hashtag
AFTER INSERT
ON tweet FOR EACH ROW
    BEGIN
      DECLARE tags varchar(6) ;
      SET @start_loc := 1;
      SET @start_pos := -1;
      SET @end_pos := -1;
      SET @total_len =  LENGTH(NEW.tweet_content);
      WHILE @start_loc < @total_len
      DO
        SET @start_pos := LOCATE('#',NEW.tweet_content,@start_loc);
        -- SET @end_pos := LOCATE(' ',str,@start_pos+1 );
        SET @end_pos := @start_pos + 5 ;
        SET @s := SUBSTRING(NEW.tweet_content, @end_pos + 1 , 1);

        IF @start_pos >= 1 AND @end_pos > 0 THEN
          -- SET @len = @end_pos - @start_pos + 1;
            SET @len = 6;
            SET tags := SUBSTRING(NEW.tweet_content, @start_pos, @len);
            IF @s = ' ' OR @end_pos = @total_len THEN
                INSERT INTO hashtag(hashtag, tweetid) VALUES (tags, NEW.tweetid);
            END IF;
            SET @start_loc = @end_pos+1;
        ELSE
          SET @start_loc := @total_len+1;
        END IF;

      END WHILE;
END//