import jieba as jb
from os.path import os
from jieba import posseg as psg
from xlwt.Workbook import Workbook
import jieba.analyse
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# read baidu stopwords txt and convert it to list
def get_stopswords():
    stopwords = [line.strip() for line in open(
        './stopwords-master/baidu_stopwords.txt',
        encoding='utf-8'
    ).readline()]
    return stopwords


# split comments
def segment(sentence):
    print('sentence: {}'.format(sentence))
    # process txt with jieba
    sentence_seg = jb.cut(sentence.strip())
    # get stopwords
    stopwords = get_stopswords()
    output_string = ''
    # remove stopwords
    for word in sentence_seg:
        if word not in stopwords:
            if word != '\t':
                output_string += word
                output_string += ' '
    print('output_string: {}'.format(output_string))
    return output_string


# comments txts in one single folder
def get_comments_folder():
    # define the comments folder path
    # pos comments folder here
    folder_path = 'F:\\蔡觐阳\\Programming\\Python\\MachineLearning\\nlp\\pos\\'
    # get all the files in this folder path
    comments_folder = os.listdir(folder_path)
    # new a list to store txt files
    file_lists = []
    for f in comments_folder:
        if(os.path.isfile(folder_path + '/' + f)):
            # check the suffix of txts
            if os.path.splitext(f)[1] == '.txt':
                file_lists.append(f)
    print('file_lists: {}', file_lists)
    return folder_path, file_lists


# comments in one single txt
def get_comments_file():
    # define the comments txt file path
    file_path = './comments.txt'
    comments_file = open(file_path, 'r', encoding='utf-8').read()
    print('comments_file: {}', comments_file)
    # print the properties of segments in comments_file
    print([(x.word, x.flag) for x in psg.cut(comments_file)])
    return comments_file


# generate excel
def excel_generator(folder_path, file_lists):
    # define a list to store the excel row data
    excel_list = []
    for txt_file_name in file_lists:
        comments_file = open(folder_path + txt_file_name,
                             'r',
                             encoding='utf8',  # Zh - utf8, Eng - gbk
                             errors='ignore')
        comments = comments_file.readlines()
        print(comments)
        # close the file to ensure the security
        comments_file.close()

        str = ''
        for line in comments:
            str += line
            str = str.strip()
        print(str)
        # strip str then push segments into list
        str = segment(str)
        str = str.strip()
        row_seg_list = []
        row_seg_list.append(str)
        print("row_seg_list: {}", row_seg_list)

        # define lebal to show how postive or negtive the comment is
        label = 0
        # combine label value and row_seg_list, then assign excel_list
        row_seg_list.append(label)
        excel_list.append(row_seg_list)

    # excel表格式
    book = Workbook()
    sheet1 = book.add_sheet('evaluation')
    row0 = ['comments_segments', 'label']

    for i in range(len(row0)):
        sheet1.write(0, i, row0[i])

    # 两个for循环，第一个for循环针对写入excel的每行，第二个for循环针对每行的各列
    for i, li in enumerate(excel_list):
        print('i:{}, li:{}'.format(i, li))
        for j, lj in enumerate(li):
            sheet1.write(i+1, j, lj)
    # 数据存入excel文件
    book.save('pos_fenci_excel.xls')


# define a filter to filter useless words
def filter(comments_file):
    # 载入自定义词典
    jb.load_userdict('./dict.txt')
    # 载入自定义停止词
    jb.analyse.set_stop_words('./stopwords-master/baidu_stopwords.txt')
    # 去掉中英文状态下的逗号、句号

    # define the useless parts of speechs
    # the table from jieba page
    # n   普通名词    f   方位名词      s   处所名词     t   时间
    # nr  人名        ns  地名         nt  机构名       nw  作品名
    # nz  其他专名    v   普通动词      vd  动副词       vn  名动词
    # a   形容词      ad  副形词	   an  名形词       d	副词
    # m   数量词      q   量词	       r   代词         p	介词
    # c   连词        u   助词	       xc  其他虚词     w   标点符号
    # PER 人名        LOC 地名	       ORG 机构名       TIME    时间
    nowords = ['x', 'uj', 'ul', 'p', 'd', 'v', 'zg', 'm',
               'ug', 'i', 'f', 'ad', 'nz', 'r', 'q', 't', 'c']
    # print the parts of speechs in comments
    print([(x.word, x.flag) for x in psg.cut(comments_file)])
    # remove punctuations
    comments_file = comments_file.strip()
    comments_file = comments_file.replace('、', '')
    comments_file = comments_file.replace('，', '。')
    comments_file = comments_file.replace('《', '。')
    comments_file = comments_file.replace('》', '。')
    comments_file = comments_file.replace('～', '')
    comments_file = comments_file.replace('…', '')
    comments_file = comments_file.replace('\r', '')
    comments_file = comments_file.replace('\t', ' ')
    comments_file = comments_file.replace('\f', ' ')
    comments_file = comments_file.replace('/', '')
    comments_file = comments_file.replace('、', ' ')
    comments_file = comments_file.replace('/', '')
    comments_file = comments_file.replace('。', '')
    comments_file = comments_file.replace('（', '')
    comments_file = comments_file.replace('）', '')
    comments_file = comments_file.replace('_', '')
    comments_file = comments_file.replace('?', ' ')
    comments_file = comments_file.replace('？', ' ')
    comments_file = comments_file.replace('了', '')
    comments_file = comments_file.replace('➕', '')
    comments_file = comments_file.replace('：', '')
    # remove characters whose len < 2
    words = [x.word for x in psg.cut(comments_file)
             if len(x.word) >= 1 and (x.flag) not in nowords]
    print(words)
    return words


# words count to generate word cloud
def count_words_from_comments(words):
    words_count = Counter(words)
    return words_count


# word cloud generator
def word_cloud_generator(words_count):
    word_cloud = WordCloud(background_color='white',                    # 设置背景颜色
                           # mask = pic,                                # 设置背景图片
                           max_words=40,                                # 设置最大现实的字数
                           # stopwords =STOPWORDS.add('有点')           # 设置停用词
                           font_path='microsoft_yahei.ttf',             # 设置字体格式，如不设置显示不了中文
                           max_font_size=80,                            # 设置字体最大值
                           random_state=200,                            # 设置有多少种随机生成状态，即有多少种配色方案
                           relative_scaling=1,
                           scale=10).generate_from_frequencies(words_count)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()
    word_cloud.to_file("词云.jpg")


comments = get_comments_file()
print(comments)
words = filter(comments)
words_count = count_words_from_comments(words)
word_cloud_generator(words_count)


# get_comments_folder()
# folder_path = ''
# file_lists = []
# folder_path,  file_lists = get_comments_folder()
# excel_generator(folder_path, file_lists)
