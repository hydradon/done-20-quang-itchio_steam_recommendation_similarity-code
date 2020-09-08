library(jsonlite)

precision <- fromJSON("../scripts/result1.json", flatten=TRUE)

# Genre specific - Action, Adventure, Visual Novel, Role Playing
action <- precision[grepl("Action", precision[["genres"]]), ]
adventure <- precision[grepl("Adventure", precision[["genres"]]), ]
platformer <- precision[grepl("Platformer", precision[["genres"]]), ]
puzzle <- precision[grepl("Puzzle", precision[["genres"]]), ]
roleplaying <- precision[grepl("Role Playing", precision[["genres"]]), ]
visual_novel <- precision[grepl("Visual Novel", precision[["genres"]]), ]
simulation <- precision[grepl("Simulation", precision[["genres"]]), ]

shooter <- precision[grepl("Shooter", precision[["genres"]]), ]
strategy <- precision[grepl("Strategy", precision[["genres"]]), ]
survival <- precision[grepl("Survival", precision[["genres"]]), ]
interactive_fiction <- precision[grepl("Interactive Fiction", precision[["genres"]]), ]
card_game <- precision[grepl("Card Game", precision[["genres"]]), ]



mixAlgo_genre_ap5 <- data.frame(
  Genre = c(  rep("Action",length(action$mix_ap5)), 
              rep("Adventure",length(adventure$mix_ap5)), 
              rep("Platformer",length(platformer$mix_ap5)), 
              rep("Puzzle", length(puzzle$mix_ap5)), 
              # rep("Roleplaying",length(roleplaying$mix_ap5)),
              rep("Visual Novel", length(visual_novel$mix_ap5))
              # rep("Simulation", length(simulation$mix_ap5)),
              # rep("Shooter", length(shooter$mix_ap5)),
              # rep("Strategy", length(strategy$mix_ap5)),
              # rep("Survival", length(survival$mix_ap5)),
              # rep("Card Games", length(card_game$mix_ap5)),
              # rep("Interactive Fiction", length(interactive_fiction$mix_ap5))
              
            ),
  # Precision = c( action$mix_p5,
  #                adventure$mix_p5,
  #                platformer$mix_p5,
  #                puzzle$mix_p5,
  #                roleplaying$mix_p5,
  #                visual_novel$mix_p5,
  #                simulation$mix_p5,
  #                shooter$mix_p5,
  #                strategy$mix_p5,
  #                # survival$mix_ap5,
  #                # card_game$mix_p5,
  #                interactive_fiction$mix_ap5
  #               )
  Precision = c( action$tag_ap5,
                 adventure$tag_ap5,
                 platformer$tag_ap5,
                 puzzle$tag_ap5,
                 # roleplaying$tag_ap5,
                 visual_novel$tag_ap5
                 # simulation$tag_ap5,
                 # shooter$tag_ap5,
                 # strategy$tag_ap5,
                 # survival$mix_ap5,
                 # card_game$mix_ap5,
                 # interactive_fiction$tag_ap5
  )
)


library(ggplot2)
ggplot(mixAlgo_genre_ap5, aes(x=Genre, y=Precision)) +
  geom_boxplot() +
  theme(
    panel.border = element_blank(),  
    # Remove panel grid lines
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    # Remove panel background
    panel.background = element_blank(),
    legend.position = "none",
    axis.line = element_line(),
    axis.title.x = element_blank(),
    axis.text.x = element_text(angle = 30, hjust=1)
  ) +
  ylab("AP@5")





# Plot genre count for genre reason
library(dplyr) 
genre_reasons_count <- read.csv("../dataset/reason_no_match_genres_count.csv", 
                                encoding = "UTF-8" ,
                                stringsAsFactors = FALSE,
                                na.strings=c("","NA"))
names(genre_reasons_count)[names(genre_reasons_count)=="X.U.FEFF.genre"] <- "Genre"
names(genre_reasons_count)[names(genre_reasons_count)=="count"] <- "Number"

genre_reasons_count <- genre_reasons_count[order(-genre_reasons_count$Number),]

# top_n(genre_reasons_count, n=12, Number) %>% 
ggplot(data=genre_reasons_count, 
       aes(x=reorder(Genre, Number), 
           y=Number)) +
  geom_bar(stat="Identity", width=0.7) +
  theme(
    panel.border = element_blank(),  
    # Remove panel grid lines
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    # Remove panel background
    panel.background = element_blank(),
    axis.line = element_line(),
    axis.title.y = element_blank(),
    axis.text=element_text(size=12, face="bold"),
    axis.title=element_text(size=14),
    # axis.text.x = element_text(angle = 30, hjust=1)
  ) +
  geom_text(aes(label=Number, fontface=2), hjust=-0.2, vjust=0.38) +
  ylab("# of games") +
  coord_flip()

ggsave("../../wip-20-quang-itch-steam-recommendation-text/figs/reasons-genre-count-3.8x6.pdf", 
       width = 6, height = 3, device=cairo_pdf)

