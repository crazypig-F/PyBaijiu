Sys.setlocale(category = 'LC_ALL', locale = 'English_United States.1252')
library(forcats)
source("./plot/font.R")
source("./plot/color.R")

data <- read.csv("./data/temp/宏转录组种水平top20相对丰度.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
data$Strains <- fct_inorder(data$Strains)
data$Samples <- fct_inorder(data$Samples)

COLOR <- COLOR[1:nlevels(data$Strains) - 1]
COLOR <- append(COLOR, COLOR_END)
g <- ggplot(data, aes(x = Samples, y = Values, fill = Strains)) +
  geom_col(position = 'stack', width = 0.9) + # stack：堆叠图
  scale_fill_manual(values = COLOR) +
  scale_y_continuous(limits = c(-.1, 100.1), expand = c(0, 0)) +
  scale_x_discrete(expand = c(0, 0)) +
  theme_bw() +
  labs(fill = "", x = "", y = "")+
  guides(fill = guide_legend( ncol = 1, byrow = TRUE))

g + p
ggsave(filename = "./pdf/transcriptome stack species.pdf", g + p, width = 35, height = 20, dpi = 600, units = "cm", device = 'pdf')
