Sys.setlocale(category = 'LC_ALL', locale = 'English_United States.1252')
library(vegan)
library(ggrepel)
library(ggplot2)
library(forcats)

bacteria <- read.csv("./data/temp/大曲所有微生物机械车间样品平均.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
physicochemical <- read.csv("./data/temp/大曲理化机械车间样品平均.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE) #读取响应变量数据
mapping <- read.csv("./mapping/sample_mapping_mean.csv", header = TRUE, row.names = 1, encoding = "UTF-8", check.names = FALSE)
bacteria <- t(bacteria)
mapping <- mapping[rownames(bacteria),]

#根据DCA1的Axis Lengths值进行选择，如果>4.0选CCA；如果在3.0-4.0之间，选RDA和CCA都可以；如果<3.0, 选择RDA分析即可。
print(decorana(bacteria))

RDA <- rda(bacteria, physicochemical, scale = T)
#提取样本得分
df_rda <- data.frame(RDA$CCA$u[, 1:2], rownames(physicochemical))
colnames(df_rda) <- c("RDA1", "RDA2", "samples")
# 提取物种得分
df_rda_species <- data.frame(RDA$CCA$v[, 1:2])
#提取环境因子得分
df_rda_env <- RDA$CCA$biplot[, 1:2]
df_rda_env <- as.data.frame(df_rda_env)

#计算轴标签数据（=轴特征值/sum(所有轴的特征值)）
RDA1 <- round(RDA$CCA$eig[1] / sum(RDA$CCA$eig) * 100, 2)
RDA2 <- round(RDA$CCA$eig[2] / sum(RDA$CCA$eig) * 100, 2)


#将绘图数据和分组合并
df_rda["Group"] <- mapping["Phase"]
df_rda$Group <- fct_inorder(df_rda$Group)
df_rda_env["name"] <- c("starch", "moisture", "glycating power", "vat sugars", "total acid", "total esters")
color <- c("#1597A5", "#FFC24B", "#FEB3AE", "#F533AD") #颜色变量


g <- ggplot() + #指定数据、X轴、Y轴，颜色
  geom_point(data = df_rda, aes(x = RDA1, y = RDA2, color = Group), size = 3, shape = 16) + #绘制点图并设定大小
  # geom_text_repel(data = df_rda,
  #                 aes(RDA1, RDA2, label = samples, color = Group), size = 3.5,
  #                 box.padding = 0.2, #字到点的距离
  #                 point.padding = 0.2, #字到点的距离，点周围的空白宽度
  #                 min.segment.length = 0.5, #短线段可以省略
  #                 segment.color = "#545454",
  #                 segment.size = 0.4,
  #                 force = T,
  # ) +
  stat_ellipse(data = df_rda,
               aes(RDA1, RDA2, color = Group),
               level = 0.95,
               linetype = 2, size = 1,
               show.legend = F) +
  geom_segment(data = df_rda_env, aes(x = 0, y = 0, xend = df_rda_env[, 1], yend = df_rda_env[, 2]),
               color = "#B56748", linetype = 1, size = 1, arrow = arrow(angle = 35, length = unit(0.3, "cm"))) +
  geom_text_repel(data = df_rda_env,
                  aes(RDA1, RDA2, label = name), size = 5,
                  box.padding = 0.2, #字到点的距离
                  point.padding = 0.2, #字到点的距离，点周围的空白宽度
                  min.segment.length = 0.5, #短线段可以省略
                  segment.color = "#545454",
                  segment.size = 0.4,
                  force = T
  ) +
  geom_point(data = df_rda_species, aes(RDA1, RDA2), color = "#605399", size = 2) +
  geom_text_repel(data = df_rda_species,
                  aes(RDA1, RDA2, label = rownames(df_rda_species)), size = 3,
                  box.padding = 0.2, #字到点的距离
                  point.padding = 0.2, #字到点的距离，点周围的空白宽度
                  min.segment.length = 0.5, #短线段可以省略
                  segment.color = "#545454",
                  segment.size = 0.4,
                  force = T,
                  fontface = "italic"
  ) +
  scale_color_manual(values = color) + #点的颜色设置
  scale_fill_manual(values = color) +
  labs(x = paste0("RDA1 (", RDA1, "%)"),
       y = paste0("RDA2 (", RDA2, "%)")) + #将x、y轴标题改为贡献度
  geom_vline(xintercept = 0, lty = "dashed") +
  geom_hline(yintercept = 0, lty = "dashed") + #图中虚线
  xlim(-1.1, 1.1) +
  ylim(-1, 0.5) +
  theme_bw() #主题设置

g + p
ggsave(filename = "./pdf/RDA mechanical all.pdf", g + p, width = 25, height = 20, dpi = 600, units = "cm", device = 'pdf')
