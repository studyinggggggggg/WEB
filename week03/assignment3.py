import requests
from bs4 import BeautifulSoup


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

genie = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number

for i in genie:
    s_name = i.select_one('td.check > input')['title']

    s_rank = i.select_one('td.number')
    s_rs = s_rank.text.strip('')
    s_sing = i.select_one('td.info > a.artist.ellipsis').text
    if(s_rs[1] == '\n'):
        print(s_rs[0] , ' ', s_name, ' ', s_sing)
    else:
        print(s_rs[0:2], ' ', s_name, ' ', s_sing)
