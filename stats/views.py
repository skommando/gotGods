from django.shortcuts import render
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests

users = [
    r"闲闲小可爱",
    r"基拉的左轮",
    r"云天挽歌",
    r"我爱两仪式",
    r"菠萝快乐车",
    r"丨ELUNE丨",
    r"技不如人，甘拜下风。",
    r"相思寄于山海",
    r"忧伤暗火",
    r"喵了個咪的",
    r"三谷加奈惠",
    #r"Nirvana_Y"
]

def index(request):
    latest_stats_list = []
    for user in users:
        stat = {}
        userId = quote(user)
        # print(userId)
    
        # 拉数据
        stat = {}
        url = "http://wotbox.ouj.com/wotbox/index.php?r=default%2Findex&pn={id}".format(id=userId)
        resp = requests.get(url)
        webContent = resp.content
        soup = BeautifulSoup(webContent, 'html.parser')

        stat["id"] = user
        stat["power"] = soup.find(class_='power fl').span.get_text()
        stat["win_rate"] = soup.find(class_='title win-rate-1k').next_sibling.next_sibling.get_text()
        stat["win_rate_c"] = 1 if int(soup.find(class_='title win-rate-1k').next_sibling.next_sibling.get_text().strip('%')) >= 50 else 0 
        stat["total"] = soup.find(class_='total').get_text()[2:]
        stat["win"] = soup.findAll(class_="win")[5].get_text()[2:]
        stat["fail"] = soup.find(class_='fail').get_text()[2:]
        stat["damage"] = soup.findAll(class_='num')[6].get_text()
        stat["exp"] = soup.findAll(class_='num')[7].get_text()
        stat["destroy"] = soup.findAll(class_='num')[8].get_text()
        stat["discover"] = soup.findAll(class_='num')[11].get_text()
        stat["level"] = soup.find(class_='title avg-lv-1k').next_sibling.next_sibling.get_text()
        stat["hit_rate"] = soup.find(class_='title hit-rate-1k').next_sibling.next_sibling.get_text()
        for i in range(5):
            stat["p{n}c".format(n=i+1)] = 1 if soup.findAll(class_='recent-list__right')[i].td.get_text() == '胜利' else 0 
            stat["p{n}".format(n=i+1)] = soup.findAll(class_='recent-list__right')[i].td.next_sibling.next_sibling.get_text()
        print(stat)        
        latest_stats_list.append(stat)
    context = {
        'latest_stats_list': latest_stats_list,
    }
    return render(request, 'stats/index.html', context)
