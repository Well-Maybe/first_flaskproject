import sys
import pymysql
from bs4 import BeautifulSoup  # 网页解析获取数据
import re  # 正则表达式
import urllib.request, urllib.error  # 制定url获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行数据库操作
'''
#数据库创建语句
CREATE TABLE `movie250` (
`id`  int NOT NULL AUTO_INCREMENT ,
`link`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`imglink`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`rating`  float NULL DEFAULT NULL ,
`judge`  int NULL DEFAULT NULL ,
`inq`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`bd`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`title`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
`otitle`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
ROW_FORMAT=DYNAMIC
;
'''
# 创建正则表达式对像
find_Link = re.compile(r'<a href="(.*?)">')
find_Img = re.compile(r'<img .* src="(.*?)"', re.S)  # 忽略换行符
find_Title = re.compile(r'<span class="title">(.*?)</span>')
find_Rating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
find_Judge = re.compile(r'<span>(\d*)人评价</span>')
find_Inq = re.compile(r'<span class="inq">(.*)</span>')
find_Bd = re.compile(r'<p class="">(.*?)</p>', re.S)
# 数据库链接配置
HOST = 'localhost'
USER = 'root'
PASSWORD = '123'
DATABASE = 'pypc'

def main():
    base_url = 'https://movie.douban.com/top250?start='
    # # 爬取网页
    datalist = getData(base_url)
    # 解析数据
    # ask_URL(base_url)
    # 保存数据
    saveDataDb(datalist)


def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数
        url = baseurl + str(i * 25)
        html = ask_URL(url)
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='item'):  # 查找符合要求的字符串形成列表
            data = []
            item = str(item)
            link = re.findall(find_Link, item)[0]
            data.append(link)
            img = re.findall(find_Img, item)[0]
            data.append(img)
            title = re.findall(find_Title, item)
            if len(title) == 2:
                c_title = title[0]
                data.append(c_title)

                o_title = title[1].replace("/", "")
                data.append(o_title)
            else:
                data.append(title[0])
                data.append('')
            rating = re.findall(find_Rating, item)[0]
            data.append(rating)
            judge = re.findall(find_Judge, item)[0]
            data.append(judge)
            inq = re.findall(find_Inq, item)
            if len(inq) != 0:
                data.append(inq[0].replace('。', ''))
            else:
                data.append('')
            bd = re.findall(find_Bd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', '', bd)  # 去掉br
            bd = re.sub('/', '', bd)
            data.append(bd.strip())  # 去掉前后空格
            datalist.append(data)

            # print(rating)

    return datalist


def saveData(datalist):
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建workbook对象
    worksheet = workbook.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ('电影详情链接', '图片链接', '影片中文名', '影片外国名', '评分', '评价数', '概况', '相关信息')
    for i in range(0, 8):
        worksheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        print('第%d条' % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            worksheet.write(i + 1, j, data[j])

    workbook.save('student.xls')  # 保存文件


def ask_URL(url):
    # 模拟浏览器头部消息，向豆瓣服务器发送消息
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
    # 用户代理，告诉服务器我们是什么类型的机器浏览器
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
    return html




conn = ''


def saveDataDb(datalist):
    global conn
    try:
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        cur = conn.cursor()
        for data in datalist:
            for index in range(len(data)):
                if index == 4 or index == 5:
                    continue
                data[index] = '"' + data[index] + '"'
            sql = '''INSERT INTO movie250 (link, imglink,title,otitle ,rating, judge, inq, bd) VALUES (%s)''' % ','.join(
            data)
            #print(sql)
            cur.execute(sql)
            conn.commit()
    except pymysql.Error as e:
        print(e)
    conn.close()


if __name__ == '__main__':
    main()
    print('爬取完毕')
