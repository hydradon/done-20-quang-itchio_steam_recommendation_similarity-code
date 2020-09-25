USE gamerecs;

-- read only user
CREATE USER 'normuser'@'%' IDENTIFIED BY 'quangNorm9)';
GRANT SELECT ON gamerecs.* TO 'normuser'@'%';

-- rating user
CREATE USER 'rater'@'%' IDENTIFIED BY 'quangRater9)';
GRANT INSERT ON gamerecs.rec_ratings TO 'rater'@'%';

FLUSH PRIVILEGES;
