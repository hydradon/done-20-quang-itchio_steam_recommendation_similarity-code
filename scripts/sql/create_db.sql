CREATE DATABASE IF NOT EXISTS gamerecs 
CHARACTER SET = utf8mb4 
COLLATE = utf8mb4_unicode_ci;

USE gamerecs;

CREATE TABLE IF NOT EXISTS `toprecs`
(
	`itch_game` VARCHAR(255),
    `itch_game_url` VARCHAR(255),
    `steam_game` VARCHAR(255),
	`steam_game_index` INT,
    `steam_game_url` VARCHAR(255),
    `sim_scores` FLOAT,
    `game_desc_snippet` TEXT,
    `game_no_ratings` INT,
    `row_id` INT
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `rec_ratings`
(
	`itch_game_url` VARCHAR(255),
    `steam_game_url` VARCHAR(255),
    `is_upvote` BOOLEAN,
    `feedback` TEXT,
    `overall_feedback` TEXT,
    `u_id` VARCHAR(64),
    `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `game_twitter_devs`
(
	`game_name` VARCHAR(255),
	`game_url` VARCHAR(255),
    `main_twitter_link` VARCHAR(255),
    `uid` VARCHAR(64),
    `dev_itch_link` VARCHAR(255),
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
