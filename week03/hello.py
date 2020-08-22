import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta


url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303'

data = requests.get(url)

soup = BeautifulSoup(data.text, 'html.parser')


#nth-child는 오류 발생 nth-child 를 nth-of-type으로 변경..

a = soup.select('#old_content > table > tbody > tr')
for i in a:
    a_tag = i.select_one('td.title > div > a')
    n_tag = i.select_one('td:nth-of-type(1) > img')
    r_tag = i.select_one('td.point')
    if(a_tag is not None):
        title = a_tag.text
        ranking = r_tag.text
        nb = n_tag['alt']
        doc = {
            'num' : nb ,
            'title' : title,
            'rank' : ranking
        }
        db.movies.insert_one(doc)


matrix = db.movies.find_one({'title' : '매트릭스'})
print(matrix['rank'])

same_aver = list(db.movies.find({'rank': '9.39'},{'_id':False}))
for i in same_aver:
    print(i['title'])



db.movies.update_one({'title':'매트릭스'},{'$set':{'rank':'0.0'}})






