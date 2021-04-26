from flask import Flask, render_template
import pymysql

HOST = 'localhost'
USER = 'root'
PASSWORD = '123'
DATABASE = 'pypc'

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return index()


@app.route('/score')
def score():
    list_rating = []
    list_num = []
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cur = conn.cursor()
    sql = "SELECT rating,count(rating) FROM movie250 group by rating;"
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        list_rating.append(str(item[0]))
        list_num.append(item[1])
    cur.close()
    conn.close()
    return render_template('score.html', list_num=list_num, list_rating=list_rating)


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/word')
def word():
    return render_template('word.html')


@app.route('/movie')
def movie():
    datalist = []
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
    cur = conn.cursor()
    sql = "SELECT * FROM movie250;"
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()

    return render_template("movie.html", movies=datalist)


if __name__ == '__main__':
    app.run()
