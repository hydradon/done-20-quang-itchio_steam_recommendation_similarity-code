library(jsonlite)
library(distdiff)
library(effsize)
# precision <- fromJSON("../scripts/result.json", flatten=TRUE)

precision <- fromJSON("../scripts/result1.json", flatten=TRUE)


# Average Precision at 5
wilcox.test(precision$tag_ap5, precision$mix_ap5, alternative = "greater")
comp.dist.plot(precision$tag_ap5,  precision$mix_ap5,
               legend1 = "Tag weighted",legend2 = "Mix",legendpos = "topleft", cut = FALSE)
# == Mix vs Genre and Mix vs Desc
wilcox.test(precision$mix_ap5, precision$genre_ap5, alternative = "greater")
comp.dist.plot(precision$genre_ap5, precision$mix_ap5,
               legend1 = "Genre weighted", legend2 = "Mix", legendpos = "topleft", cut = FALSE)
cliff.delta(precision$mix_ap5, precision$desc_ap5)

wilcox.test(precision$mix_ap5, precision$desc_ap5, alternative = "greater")
comp.dist.plot(precision$desc_ap5, precision$mix_ap5,
               legend1 = "Desc weighted", legend2 = "Mix", legendpos = "topleft", cut = FALSE)
cliff.delta(precision$mix_ap5, precision$tag_ap5)

# == Tag vs Genre and Tag vs Desc
par(mar = c(2,0.4,0.1,0.1))
wilcox.test(precision$tag_ap5, precision$genre_ap5, alternative = "greater")
comp.dist.plot(precision$tag_ap5, precision$genre_ap5,
               legend1 = "Tag weighted", legend2 = "Genre weighted", legendpos = "topright", cut = FALSE)
cliff.delta(precision$tag_ap5, precision$genre_ap5)

wilcox.test(precision$tag_ap5, precision$desc_ap5, alternative = "greater")
comp.dist.plot(precision$tag_ap5, precision$desc_ap5,
               legend1 = "Tag weighted", legend2 = "Desc weighted", legendpos = "topright", cut = FALSE)
cliff.delta(precision$tag_ap5, precision$desc_ap5)



library(ggplot2)


summary(precision$tag_ap5)
summary(precision$genre_ap5)
summary(precision$desc_ap5)
summary(precision$mix_ap5)


all_algo <- data.frame(
  Weight = rep(c("x = tag","x = genre", "x = desc", "x = mix"), each = length(precision$mix_ap5)),
  Precision = c(precision$tag_ap5, precision$genre_ap5, precision$desc_ap5, precision$mix_ap5)
)

ggplot(all_algo, aes(x=Weight, y=Precision)) + 
  geom_boxplot() +
  # facet_wrap(~Metrics, scale="free") +
  theme(strip.text.x = element_blank(),
        panel.border = element_blank(),  
        # Remove panel grid lines
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        # Remove panel background
        panel.background = element_blank(),
        # legend.position = "none",
        axis.text=element_text(size=14, face="bold"),
        axis.title=element_text(size=16),
        axis.line = element_line()
  ) +
  ylab("AP@5") + 
  xlab(expression(italic('score'['overall,x']))) +
  coord_flip()

ggsave("../../wip-20-quang-itch-steam-recommendation-text/figs/compare-algo.pdf", 
       width = 6, height = 1.9, device=cairo_pdf)



