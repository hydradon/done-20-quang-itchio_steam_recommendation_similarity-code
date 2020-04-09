all_games <- read.csv("../dataset/game_details_raw.csv",
                           encoding = "UTF-8" ,
                           stringsAsFactors = FALSE,
                           na.strings=c("","NA"))

all_games$game_desc_len[is.na(all_games$game_desc_len)] <- 0
plot(density(all_games$game_desc_len))
summary(all_games$game_desc_len)
