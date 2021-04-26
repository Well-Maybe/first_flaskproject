import jieba  # 分词
from matplotlib import pyplot as plt  # 绘图
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import pymysql

HOST = 'localhost'
USER = 'root'
PASSWORD = '123'
DATABASE = 'pypc'
conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
cur = conn.cursor()
sql = 'select inq FROM movie250'
cur.execute(sql)
data = cur.fetchall()
text = ''
for item in data:
    text = text + item[0]
# print(text)
cur.close()
conn.close()
# 分词
cut = jieba.cut(text)
string = " ".join(cut)
print(len(string))

# 相关遮罩图片
img = Image.open(r'static/assets/img/tree.jpg')  # 打开遮罩图片
img_array = np.array(img)  # 将图片转换为数组
wc=WordCloud(
    background_color='white',
    mask=img_array,
    font_path='simhei.ttf'
)
wc.generate_from_text(string)

#绘制图片
fig=plt.figure(1)
plt.imshow(wc)
plt.axis('off')#是否显示坐标轴
# plt.show()
plt.savefig(r'static/assets/img/output.jpg',dpi=500)