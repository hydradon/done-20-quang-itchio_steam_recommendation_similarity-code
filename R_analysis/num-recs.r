library(ggplot2)

num_recs <- read.csv("../dataset/num_recs.csv", 
                       encoding = "UTF-8" ,
                       stringsAsFactors = FALSE,
                       na.strings=c("","NA"))

ggplot(num_recs, aes(x=counts)) +
  # stat_density(aes(y=..count..)) +
  # geom_density() +
  geom_bar(width=0.7) +
  theme(
    panel.border = element_blank(),  
    # Remove panel grid lines
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    # Remove panel background
    panel.background = element_blank(),
    axis.line = element_line(),
    axis.text=element_text(size=12, face="bold"),
    axis.title=element_text(size=14),
  ) +
  labs(x = "# of matched Steam games",
       y= "# of indie games") +
  scale_x_continuous(breaks=5:15)
  # xlab("Number of matched Steam games")

ggsave("../../wip-20-quang-itch-steam-recommendation-text/figs/number-Steam-matched.pdf", 
       width = 6, height = 1.9, device=cairo_pdf)
