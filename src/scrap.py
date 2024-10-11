import requests
from bs4 import BeautifulSoup
from telbot import TelegramBot
import asyncio, time
from params import params_list

def get_trs(params):
    baseurl = 'https://gall.dcinside.com/mgallery/board/lists'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }

    # 웹 페이지 요청
    response = requests.get(baseurl, params=params, headers=headers)

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        contents = soup.find_all('tr', class_='ub-content us-post')
        return contents
    else:
        print(f'request failed with: {response.status_code}')
  
def get_new_posts(params, last_no):
    res = []
    trs = get_trs(params)
    for tr in trs:
        no = tr['data-no']
        if int(no) > last_no:
            res.append((tr.find('a').text.strip(),"https://gall.dcinside.com"+tr.find('a', href=True)['href'], no))
    if res:
        return res, int(res[0][2])
    else:
        return [], last_no

def make_message(name, res):
    message = f'{name}\n'
    for i, (title, link, no) in enumerate(res):
        message += f'{i+1}. {title}\n{link}\n'
    return message

def make_message_each():
    message = ''
    for i, (name, params, last_no) in enumerate(params_list):
        time.sleep(2)
        res, params_list[i][2] = get_new_posts(params, last_no)
        if res:
            message += make_message(name, res)

    if message:
        return message
    else:
        return None

async def main():
    bot = TelegramBot()
    while True:
        msg = make_message_each()
        if msg:
            await bot.send_message(msg)
        await asyncio.sleep(45)

if __name__ == "__main__":
    asyncio.run(main())