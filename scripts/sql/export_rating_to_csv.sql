USE gamerecs;

SELECT itch_game_url, 
	   steam_game_url,
	   is_upvote, 
	   feedback,
	   u_id, 
	   timestamp, 
	   sim_scores, 
	   row_id
FROM (
	(SELECT 'itch_game_url' as itch_game_url, 
			'steam_game_url' as steam_game_url, 
			'is_upvote' as is_upvote, 
			'feedback' as feedback, 
			'u_id' as u_id, 
			'timestamp' as timestamp, 
			'sim_scores' as sim_scores,
			1 as which,
            'row_id' as row_id)
	UNION ALL
	(SELECT rating.itch_game_url, 
			rating.steam_game_url,
			cast(rating.is_upvote AS CHAR),
			rating.feedback,
			cast(rating.u_id AS CHAR),
			cast(rating.timestamp AS CHAR),
			cast(rec.sim_scores AS CHAR),
			2 as which,
            cast(rec.row_id AS CHAR)
	FROM rec_ratings rating JOIN toprecs rec
		ON rating.itch_game_url = rec.itch_game_url
		AND rating.steam_game_url = rec.steam_game_url)
) result
ORDER BY which, -- header comes first
		 result.itch_game_url ASC, 
         result.sim_scores + 0.0 DESC, 
         result.row_id ASC,
         result.u_id ASC, 
         result.timestamp ASC
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ratings_result.csv'
FIELDS ENCLOSED BY '"' TERMINATED BY ',' ESCAPED BY '"'
LINES TERMINATED BY '\r\n';

