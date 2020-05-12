# -*-coding=utf-8 -*-
from jieba import posseg as psg
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

f3 = open('comments.txt', 'r', encoding='utf-8').read()
print([(x.word, x.flag) for x in psg.cut(f3)]
      )               # 打印看看，找出我们不需要统计的词性。
print('f3', f3)
nowords = ['x', 'uj', 'a', 'ul', 'p', 'd', 'v', 'zg', 'm',
           'ug', 'i', 'f', 'ad', 'nz', 'r', 'r', 'ns', 'q', 't', 'c']

# n   普通名词    f   方位名词      s   处所名词     t   时间
# nr  人名        ns  地名         nt  机构名       nw  作品名
# nz  其他专名    v   普通动词      vd  动副词       vn  名动词
# a   形容词      ad  副形词	   an  名形词       d	副词
# m   数量词      q   量词	       r   代词         p	介词
# c   连词        u   助词	       xc  其他虚词     w   标点符号
# PER 人名        LOC 地名	       ORG 机构名       TIME    时间


words = [x.word for x in psg.cut(f3) if len(
    x.word) >= 2 and (x.flag) not in nowords]
# 顺便去掉长度小于2的单字，标点符号。
print('words:', words)
word_count = Counter(words)
print("word_count:", word_count)

wc = WordCloud(background_color='white',                    # 设置背景颜色
               # mask = pic,                                # 设置背景图片
               max_words=2000,                              # 设置最大现实的字数
               # stopwords =STOPWORDS.add('有点')           # 设置停用词
               font_path='microsoft_yahei.ttf',             # 设置字体格式，如不设置显示不了中文
               max_font_size=80,                            # 设置字体最大值
               random_state=200,                            # 设置有多少种随机生成状态，即有多少种配色方案
               relative_scaling=1,
               scale=10).generate_from_frequencies(word_count)
plt.imshow(wc)
plt.axis("off")
plt.show()
wc.to_file("词云.jpg")
