CREATE TABLE users (
username    VARCHAR(20) NOT NULL ,
firstName    VARCHAR(20)NOT NULL,
lastName    VARCHAR(20)NOT NULL,
birthDate    DATE NOT NULL,
registery_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
bio        Varchar(64),
followers   INT  NOT NULL DEFAULT 0,
following   INT  NOT NULL DEFAULT 0,
password VARCHAR(128) NOT NULL ,

PRIMARY KEY (username)
);


CREATE TABLE tweet(
tweetid          INT AUTO_INCREMENT,
type            CHAR(1) NOT NULL CHECK ( type in ('T', 'C')) ,
username         VARCHAR(20) NOT NULL,
tweet_content     VARCHAR(256) NOT NULL,
ref_id          INT,
timestamp_t     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
likes           INT NOT NULL DEFAULT 0,

PRIMARY KEY (tweetid),
FOREIGN KEY (username) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (ref_id) REFERENCES tweet(tweetid)
ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE message(
 mess_id            INT AUTO_INCREMENT,
 type           CHAR(1) NOT NULL CHECK ( type in ('M', 'T')) ,
 s_id           VARCHAR(20) NOT NULL ,
 r_id           VARCHAR(20) NOT NULL ,
 content        VARCHAR(256),
 ref_id         INT ,
 timestamp_t     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

PRIMARY KEY (mess_id),
FOREIGN KEY (s_id) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (r_id) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (ref_id) REFERENCES tweet(tweetid)
ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE login_record(
  username      VARCHAR(20) NOT NULL ,
  timestamp_t     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

PRIMARY KEY (username, timestamp_t),
FOREIGN KEY (username) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE follow (
follower    VARCHAR(20) NOT NULL ,
following    VARCHAR(20) NOT NULL ,

PRIMARY KEY (follower, following),
FOREIGN KEY (follower) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE ,
FOREIGN KEY (following) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE hashtag
(
  hashtag char(6) CHECK ( 1 = REGEXP_LIKE(UPPER(hashtag), '#[A-Z][A-Z][A-Z][A-Z][A-Z]')),
  tweetid INT,

  PRIMARY KEY (hashtag, tweetid),
  FOREIGN KEY (tweetid) REFERENCES tweet(tweetid)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE likes (
username        VARCHAR(20),
tweetid           INT,
timeStamp_l   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

PRIMARY KEY     (tweetid, username),
FOREIGN KEY     (tweetid) REFERENCES tweet(tweetid)
ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY     (username) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE block(
username        VARCHAR(20),
blocked_user     VARCHAR(20),

PRIMARY KEY (username, blocked_user ),
FOREIGN KEY (username) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE ,
FOREIGN KEY (blocked_user) REFERENCES users(username)
ON DELETE CASCADE ON UPDATE CASCADE
);

