import grequests
import requests
from bs4 import BeautifulSoup
import json


Url = input('Paste the link to your anime list: ')
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36', 'accept': '*/*'}
links = []
duration_list = []


def main():
    r = requests.get(url=Url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find('table', class_='list-table').get('data-items')
    items = json.loads(items)
    for item in items:
        links.append('https://myanimelist.net/anime/' + str(item['anime_id']))
    response = (grequests.get(url) for url in links)
    resp = grequests.map(response)
    for res in resp:
        soup = BeautifulSoup(res.text, 'html.parser')
        episodes = int(soup.find(text='Episodes:').find_previous('div').text.strip().replace('Episodes:', ''))
        duration = soup.find(text='Duration:').find_previous('div').get_text(strip=True).replace('Duration:', '')
        if len(duration) == 5:
            hr = int(duration.replace(' hr.', '')) * 60
            duration_list.append(hr * episodes)
        elif 'hr' in duration:
            hr = int(float(duration.replace(' hr. ', '.').replace(' min.', '')))
            minutes = float(duration.replace(' hr. ', '.').replace(' min.', '')) - hr
            duration_list.append(int((hr * 60 + minutes * 100) * episodes))
        elif 'per ep.' in duration:
            minutes = int(duration.replace(' min. per ep.', ''))
            duration_list.append(minutes * episodes)
        else:
            minutes = int(duration.replace(' min.', ''))
            duration_list.append(minutes * episodes)
    sum_duration = sum(duration_list) / 60
    print(f'{int(sum_duration)} hr.{int(60 * (sum_duration - int(sum_duration)))} min.')


if __name__ == '__main__':
    main()
