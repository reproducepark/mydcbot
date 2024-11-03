import requests
from bs4 import BeautifulSoup
from telbot import TelegramBot
import asyncio, time, logging
from params import params_list
from fake_useragent import UserAgent
ua = UserAgent(use_cache_server=True)

logging.basicConfig(filename='dcbot.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_trs(params):
    baseurl = 'https://gall.dcinside.com/mgallery/board/lists'
    headers = {
        'User-Agent': ua.random
    }

    logging.info(f"Requesting URL: {baseurl} with params: {params}")

    # 웹 페이지 요청
    response = requests.get(baseurl, params=params, headers=headers, timeout=30)

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        # BeautifulSoup 객체 생성
        soup = BeautifulSoup(response.text, 'html.parser')
        contents = soup.find_all('tr', class_='ub-content us-post')
        logging.info(f"Successfully retrieved {len(contents)} posts")
        return contents
    else:
        logging.error(f"Request failed with status code: {response.status_code}")
        return None
  
def get_new_posts(params, last_no):
    res = []
    trs = get_trs(params)
    if trs is None:
        return [], last_no
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
        try:
            msg = make_message_each()
            if msg:
                if len(msg) > 4096:
                    for i in range(0, len(msg), 4096):
                        await bot.send_message(msg[i:i+4096])
                        logging.info(f"Sent message part {i//4096 + 1}")
                else:
                    await bot.send_message(msg)
                    logging.info("Sent message")
        except Exception as e:
            logging.error(f"Error occurred : {e}")
            # await bot.send_message("Error occurred while sending message")
        finally:
            logging.info("Sleeping for 30 seconds")
            await asyncio.sleep(30)

if __name__ == "__main__":
    logging.info("Starting main program")
    asyncio.run(main())