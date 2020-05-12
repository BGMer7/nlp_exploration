# -*- encoding=utf-8 -*-   # 定义编码格式
import jieba.analyse
import jieba.posseg
import jieba
import pandas as pd


# 载入自定义词典
jieba.load_userdict('./dict.txt')
# 载入自定义停止词
jieba.analyse.set_stop_words('./stopwords-master/baidu_stopwords.txt')


# 去掉中英文状态下的逗号、句号
def clearSen(comment):
    comment = comment.strip()
    comment = comment.replace('、', '')
    comment = comment.replace('，', '。')
    comment = comment.replace('《', '。')
    comment = comment.replace('》', '。')
    comment = comment.replace('～', '')
    comment = comment.replace('…', '')
    comment = comment.replace('\r', '')
    comment = comment.replace('\t', ' ')
    comment = comment.replace('\f', ' ')
    comment = comment.replace('/', '')
    comment = comment.replace('、', ' ')
    comment = comment.replace('/', '')
    comment = comment.replace('。', '')
    comment = comment.replace('（', '')
    comment = comment.replace('）', '')
    comment = comment.replace('_', '')
    comment = comment.replace('?', ' ')
    comment = comment.replace('？', ' ')
    comment = comment.replace('了', '')
    comment = comment.replace('➕', '')
    comment = comment.replace('：', '')
    return comment


# 读取数据，具体文件路径，sep可看我直接的文章介绍
zhengce_content = pd.read_table('./comments.txt', sep='\t')
# 数据重命名
zhengce_content.columns = ['content']

# 文件写入。文件路径是指最后要写入哪个文件
outputfile = open('outcome2.txt', 'a+', encoding="utf-8")

for each in zhengce_content['content']:
    # 清除标点符号
    kk = clearSen(each)
    # posseg可标注词语的词性，最上面已经引入了
    seg_list = jieba.posseg.cut(kk)
    # seg_list的结果是generator类型，因此，如果你print(seg_list)，会出现类似
    # <generator object cut at 0x000001F03E18FB88>的结果，因此需要用for循环来遍历输出
    for word, flag in seg_list:
        print("%s  %s" % (word, flag))
    # 写出数据，注意缩进
        outputfile.write("%s  %s" % (word, flag))
# 关闭文件
outputfile.close()
