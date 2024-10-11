import requests
from bs4 import BeautifulSoup

params = {
    'id': 'sff',
    'list_num': 30,
    'sort_type': 'N',
    'search_head': 40,
    'page': 1
}

def get_trs(params):
    baseurl = 'https://gall.dcinside.com/mgallery/board/lists'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    # 웹 페이지 요청
    response = requests.get(baseurl, params=params, headers=headers)
    print(response)
    # 요청이 성공했는지 확인
    if response.status_code == 200:
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        contents = soup.find_all('tr', class_='ub-content us-post')
        return contents
    else:
        print(f'request failed with: {response.status_code}')
  
def get_new_posts(last_no):
    res = []
    trs = get_trs(params)
    for tr in trs:
        no = tr['data-no']
        if int(no) > last_no:
            res.append((tr.find('a').text.strip(),"https://gall.dcinside.com"+tr.find('a', href=True)['href']))

    print(res)
            

if __name__ == '__main__':
    last_no = 1149112
    get_new_posts(last_no)