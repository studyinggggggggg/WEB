from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def write_memo():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')
    desc = soup.select_one('meta[property="og:description"]')
    img = soup.select_one('meta[property="og:image"]')

    doc = {
            'URL' : url_receive,
            'COMMENT' : comment_receive,
            'TITLE' : title['content'],
            'DESC' : desc['content'],
            'IMG' : img['content']
        }

    db.alonememo.insert_one(doc)

    return jsonify({'result': 'success'})

@app.route('/memo', methods=['GET'])
def read_memo():
    memos = list(db.alonememo.find({}, {'_id': 0}))
    return jsonify({'result':'success', 'reviews': memos})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)