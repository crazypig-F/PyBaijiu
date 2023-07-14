Sys.setlocale(category = 'LC_ALL', locale = 'English_United States.1252')
library(ggplot2)
library(showtext)
showtext_auto(enable = TRUE)

# 载入黑体
font_add("heiti", regular = "C:\\Windows\\Fonts\\simhei.ttf")
# 载入宋体
font_add("songti", regular = "C:\\Windows\\Fonts\\simsun.ttc")
# 载入Times New Roman字体
font_add("newrom", regular = "C:\\Windows\\Fonts\\times.ttf")

p <- theme(
  axis.title = element_text(
    family = "serif", # 坐标轴字体
    face = 'bold', # 字体外形（粗斜体等）
    size = 20, # 字体大小
    lineheight = 1 # 标签行间距的倍数
  ),
  axis.text = element_text(
    family = "serif",
    face = "bold",
    size = 20
  ),
  legend.title = element_text(
    family = "serif",
    face = 'bold',
    size = 20
  ),
  legend.text = element_text(
    family = "serif",
    face = "bold",
    size = 20,
  ),
)


# font("xylab", size = fontSize, family = "dx") + #坐标轴标题
# #刻度的文字大小和字体
# font("xy.text", size = fontSize, family = "tnr") +
# #图例文字大小和字体
# font("legend.text", size = fontSize, family = "tnr") +
# #图例的标题的文字大小和字体
# font("legend.title", size = fontSize, family = "tnr") +
# #图例图标大小
# theme(legend.key.size = unit(0.1, "inches")) +
# #图表网格颜色、线形、线宽
# grids(linetype = "dashed", color = 'gray66', size = 0.1) +
# #图表外边框的线宽
# border(size = 0.3) +
# #刻度的宽度和长度还有朝向
# theme(axis.ticks = element_line(size = 0.3), axis.ticks.length = unit(-0.1, 'cm'))
