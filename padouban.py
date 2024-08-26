import hashlib
import os
import re
import requests
import pymysql
from bs4 import BeautifulSoup
def vertifyupdate(html):
    md5 = hashlib.md5()
    md5.update(html.encode('utf-8'))
    md5code = md5.hexdigest()
    print(md5code)
    old_html = ''
    html_name = 'gp.txt'
    if os.path.exists(html_name):
        with open(html_name, 'r', encoding='utf-8') as f:
            old_html = f.read()
    if md5code == old_html:
        print('数据未更新')
        return False
    else:
        with open(html_name, 'w', encoding='utf-8') as f:
            f.write(md5code)
            print('数据更新了')
            return True
qy = open('C:/Users/delapi/learngit/db.txt', mode='a', encoding='utf-8')
for i in range(1):
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)\
        Applewebkit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host':'movie.douban.com'
    }
    res = 'https://movie.douban.com/top250?start='+str(25*i)
    r = requests.get(res, headers = headers, timeout = 10)
    soup = BeautifulSoup(r.text, 'html.parser')
    div_list = soup.find_all('div', class_ = 'item')
    movies = []
    for each in div_list:
        movie = {}
        moviename = each.find('div', class_ = 'hd').a.span.text.strip()
        movie['title'] = moviename
        rank = each.find('div', class_ = 'pic').em.text.strip()
        movie['rank'] = rank
        info = each.find('div', class_ = 'bd').p.text.strip()
        info = info.replace('\n', '')
        info = info.replace(' ', '')
        info = info.replace('\xa0', '')
        director = re.findall(r'[导演:].+[主演:]', info)[0]
        director =director[3:len(director) - 3]
        movie['director'] = director
        debut_year = re.findall(r'[0-9]{4}', info)[0]
        movie['debut_year'] = debut_year
        genre = re.findall(r'[0-9]+[/].+[/].+', info)[0]
        genre = genre[genre.index('/') + 1:]
        genre = genre[genre.index('/') + 1:]
        movie['genre'] = genre
        star = each.find('div', class_ = 'star')
        star = star.find('span', class_ = 'rating_num').text.strip()
        movie['star'] = star
        movies.append(movie)
        print(movie, file=qy)
con = pymysql.connect(host='localhost', user='root',\
                      port=3306, charset='utf8') #password和database正式连接也需要写
print('连接成功->')
cursor = con.cursor()
print('开始创建表->')
cursor.execute('''create table douban
               (title char(40),
                ranking char(40),
                director char(40),
                debut_year char(40),
                genre char(100),
                star char(40))
               ''')
print('完成表的创建，下面插入数据->')
for i in movies:
    cursor.execute('insert into douban(title, ranking, director, debut_year, genre, star)'\
                   'values(%s, %s, %s, %s, %s, %s)',\
                    (i['title'], i['rank'], i['director'], i['debut_year'], i['genre'], i['star']))
print('插入数据完成')
cursor.close()
con.commit()
con.close()