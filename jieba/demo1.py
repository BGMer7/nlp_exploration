from os.path import os
from xlwt.Workbook import Workbook
import jieba


# 将停用词文档转换为停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open(
        './stopwords-master/baidu_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


# 对文档字符串进行中文分词
def seg_depart(sentence):
    print('sentence:{}'.format(sentence))
    # jieba工具分词结果
    sentence_depart = jieba.cut(sentence.strip())
    # 停用词列表
    stopwords = stopwordslist()

    # 输出结果保存至outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += ' '
    print('outstr:{}'.format(outstr))
    return outstr


# txt文档的路径

mypath = 'F:\\蔡觐阳\\Programming\\Python\\MachineLearning\\nlp\\pos\\'
myfiles = os.listdir(mypath)
print('myfiles:', myfiles)
print('-------------------------------')

# txt文档名列表
fileList = []
for f in myfiles:
    if(os.path.isfile(mypath + '/' + f)):
        if os.path.splitext(f)[1] == '.txt':
            fileList.append(f)
# 待写入excel文件的每一行组成的列表
# excellist中的元素为列表，包括分词结果和标签两部分


excellist = []
for ff in fileList:
    f = open(mypath + ff, 'r', encoding='utf8', errors='ignore')
    sourceInLines = f.readlines()
    f.close()
    str = ''
    rowList = []
    for line in sourceInLines:
        str += line
        str = str.strip()
    print('str:', str)
    print('-----------------------------------------')
    # 对str做分词
    str = seg_depart(str)
    str = str.strip()
    rowList.append(str)

    # 添加对应的标签0或1
    # rowList.append(0)
    rowList.append(1)
    excellist.append(rowList)

# excel表格式
book = Workbook()
sheet1 = book.add_sheet('Sheet1')
row0 = ['review', 'label']

for i in range(len(row0)):
    sheet1.write(0, i, row0[i])

# 两个for循环，第一个for循环针对写入excel的每行，第二个for循环针对每行的各列
for i, li in enumerate(excellist):
    print('i:{}, li:{}'.format(i, li))
    for j, lj in enumerate(li):
        sheet1.write(i+1, j, lj)
# 数据存入excel文件
# book.save('neg_fenci_excel.xls')
book.save('pos_fenci_excel.xls')
