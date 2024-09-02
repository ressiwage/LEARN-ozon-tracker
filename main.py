import click, time, os, re, requests, telebot
from telebot import types
from PIL import Image
from bs4 import BeautifulSoup
import html as h
from html.parser import HTMLParser
from config import BOT_TOKEN, ALLOWED_USERNAMES, URLS

dirname=os.path.dirname(__file__)
join = os.path.join

bot = telebot.TeleBot(BOT_TOKEN)
fname=join(dirname, 'price.txt')

class Config:
    chat_id=None
conf = Config()

cookies = {
    '__Secure-ETC': 'c1a04ce4fb078e3735a2dbb127dd7503',
    '__Secure-access-token': '5.0.uBbLfQuQTd-8VErND_LJTg.93.AWnnxzRYVO0ogM0NJMeS1E7yAX7hwkHFURgccy716UEb38LoTvRraeAVw8ccqhRRYg..20240902102319.hucupJP9ZKsh1qtdug52_BKhXaS9w9rYf_HjkvkfN9M.134ac26072ffece95',
    '__Secure-refresh-token': '5.0.uBbLfQuQTd-8VErND_LJTg.93.AWnnxzRYVO0ogM0NJMeS1E7yAX7hwkHFURgccy716UEb38LoTvRraeAVw8ccqhRRYg..20240902102319.A0ruyNtUsI2UdA362fUzfmUA8HcVFcLv6R-rySKrXjk.17198f35041ebeb10',
    '__Secure-ab-group': '93',
    '__Secure-user-id': '0',
    'xcid': 'f0f481276fc36e9eeffd3d2e79c81dfc',
    '__Secure-ext_xcid': 'f0f481276fc36e9eeffd3d2e79c81dfc',
    'ADDRESSBOOKBAR_WEB_CLARIFICATION': '1725265400',
    'rfuid': 'NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMDI4MjM3MjIzLC0xLC05ODc0NjQ3MjQsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVjJsdU16SWdOUzR3SUNoWGFXNWtiM2R6SUU1VUlERXdMakE3SUZkcGJqWTBPeUI0TmpRcElFRndjR3hsVjJWaVMybDBMelV6Tnk0ek5pQW9TMGhVVFV3c0lHeHBhMlVnUjJWamEyOHBJRU5vY205dFpTOHhNamd1TUM0d0xqQWdVMkZtWVhKcEx6VXpOeTR6TmlBeU1EQXpNREV3TnlCTmIzcHBiR3hoLGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4elpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hzWldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOVVYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpvaWNuVnVibWx1WnlKOWZYMTksNjUsNTIxMDUxOTExLDEsMSwtMSwxNjk5OTU0ODg3LDE2OTk5NTQ4ODcsLTE1NjE0ODE2NzAsNg==',
    'abt_data': '7.LJPtmpQn5szYPzEEVb84uN44yIpgRwysgfhIWzk2PBpq4FKuHLNub_7pc6v2zeohT78jy48qizli3tL5f3wCr5LjdGwfuCiAsAGiU8iDeAlL3jE2SQ-cNNDvhYC4rj2ZLm9oReuGTS6bF6wvrw0SWZdhsKD3SszassA1udmW0ToCSNgUM6xDyBH-7h3RfwEipkrVmyf1XiGCKQSFGX2CiGC9Wj-kkqE2oK-wIeWIAbxq4MjWv1hTj90hK298gKOWpQSWC4DqT8O4cjzes0lPEqJQD4vLhubQPiq39ouuqWl9vi1oBAmZZ2yokGiMHyV4hVfjF7b2YA9BhFtmLnLiGQ1-RecglshxNR0Cspcob10GoaoIu0op6kvAjkJByE_owCe7YHvaqU9ubvk3-gutTPltlgO7aOamCVKDPyOa7LmKxxFMrFkx_VHtYfIrFi-R0BmI',
    'is_cookies_accepted': '1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '__Secure-ETC=c1a04ce4fb078e3735a2dbb127dd7503; __Secure-access-token=5.0.uBbLfQuQTd-8VErND_LJTg.93.AWnnxzRYVO0ogM0NJMeS1E7yAX7hwkHFURgccy716UEb38LoTvRraeAVw8ccqhRRYg..20240902102319.hucupJP9ZKsh1qtdug52_BKhXaS9w9rYf_HjkvkfN9M.134ac26072ffece95; __Secure-refresh-token=5.0.uBbLfQuQTd-8VErND_LJTg.93.AWnnxzRYVO0ogM0NJMeS1E7yAX7hwkHFURgccy716UEb38LoTvRraeAVw8ccqhRRYg..20240902102319.A0ruyNtUsI2UdA362fUzfmUA8HcVFcLv6R-rySKrXjk.17198f35041ebeb10; __Secure-ab-group=93; __Secure-user-id=0; xcid=f0f481276fc36e9eeffd3d2e79c81dfc; __Secure-ext_xcid=f0f481276fc36e9eeffd3d2e79c81dfc; ADDRESSBOOKBAR_WEB_CLARIFICATION=1725265400; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMDI4MjM3MjIzLC0xLC05ODc0NjQ3MjQsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUp5ZFMxU1ZTSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVjJsdU16SWdOUzR3SUNoWGFXNWtiM2R6SUU1VUlERXdMakE3SUZkcGJqWTBPeUI0TmpRcElFRndjR3hsVjJWaVMybDBMelV6Tnk0ek5pQW9TMGhVVFV3c0lHeHBhMlVnUjJWamEyOHBJRU5vY205dFpTOHhNamd1TUM0d0xqQWdVMkZtWVhKcEx6VXpOeTR6TmlBeU1EQXpNREV3TnlCTmIzcHBiR3hoLGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4elpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hzWldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOVVYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpvaWNuVnVibWx1WnlKOWZYMTksNjUsNTIxMDUxOTExLDEsMSwtMSwxNjk5OTU0ODg3LDE2OTk5NTQ4ODcsLTE1NjE0ODE2NzAsNg==; abt_data=7.LJPtmpQn5szYPzEEVb84uN44yIpgRwysgfhIWzk2PBpq4FKuHLNub_7pc6v2zeohT78jy48qizli3tL5f3wCr5LjdGwfuCiAsAGiU8iDeAlL3jE2SQ-cNNDvhYC4rj2ZLm9oReuGTS6bF6wvrw0SWZdhsKD3SszassA1udmW0ToCSNgUM6xDyBH-7h3RfwEipkrVmyf1XiGCKQSFGX2CiGC9Wj-kkqE2oK-wIeWIAbxq4MjWv1hTj90hK298gKOWpQSWC4DqT8O4cjzes0lPEqJQD4vLhubQPiq39ouuqWl9vi1oBAmZZ2yokGiMHyV4hVfjF7b2YA9BhFtmLnLiGQ1-RecglshxNR0Cspcob10GoaoIu0op6kvAjkJByE_owCe7YHvaqU9ubvk3-gutTPltlgO7aOamCVKDPyOa7LmKxxFMrFkx_VHtYfIrFi-R0BmI; is_cookies_accepted=1',
    'priority': 'u=0, i',
    'referer': 'https://www.ozon.ru/product/prime-sleep-matras-finest-prestige-nezavisimye-pruzhiny-160h200-sm-1068560627/?from_sku=577249534&from_url=https%253A%252F%252Fwww.ozon.ru%252Fmy%252Forderlist&oos_search=false&__rr=1',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

params = {
    '__rr': '1',
    'abt_att': '1',
    'from_sku': '577249534',
    'from_url': 'https%3A%2F%2Fwww.ozon.ru%2Fmy%2Forderlist',
    'oos_search': 'false',
}

def get_ozon_info(url):
    try:
        txt = requests.get(
            url,
            params=params,
            headers=headers,
            cookies=cookies
        ).text
    except:
        time.sleep(60*5)
        txt = requests.get(
            url,
            params=params,
            headers=headers,
            cookies=cookies
        ).text

    soup = BeautifulSoup(txt, 'html.parser')    
    return str(
        soup.select('div[data-widget="webSale"] span:-soup-contains("₽")')[0].get_text()
    )

def main():

    while True:
        start_time = int(time.time())

        for i, url in enumerate(URLS):
            fname_=fname.rsplit('.')[0]+str(i)+'.'+fname.rsplit('.')[1]
            search=re.findall(r'[0-9]+', get_ozon_info(url))
            
            price = int(''.join(search))
            with open(f'{fname_}', 'a') as f:
                f.write(str(price)+'\n')
            with open(f'{fname_}', 'r+') as f:
                prev_prices = f.readlines()
                if len(prev_prices)>40:
                    f.seek(0)
                    f.truncate(0)
                    f.writelines(prev_prices[1:21])

            prev_prices = [int(i) for i in prev_prices]

            if len(prev_prices)!=0 and price< (sum(prev_prices)/len(prev_prices))*0.95:
                message=f'price is now {price} on url {url}, that is {int((sum(prev_prices)/len(prev_prices))/price*100)}% less than average'
                bot.send_message(conf.chat_id, message, parse_mode='Markdown')

        end_time = int(time.time())
        time.sleep(max(
            30*60 - (end_time-start_time), 1
            )) # once per half hour


@bot.message_handler(
    commands=["exit"], func=lambda message: message.chat.username in ALLOWED_USERNAMES
)
def sign_handler(message):
    exit()

@bot.message_handler(
    commands=["start"], func=lambda message: message.chat.username in ALLOWED_USERNAMES
)
def sign_handler(message):
    text = f"бот авторизован, сбор информации начат по товарам {'\n\n'.join(URLS)}"
    click.secho(text,  fg='green')
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    conf.chat_id = message.chat.id
    with open(join(dirname, 'chatid.txt'),'w+') as f:
        f.write(str(conf.chat_id))
    main()

    
with open(fname, 'w+') as f:
    f.write('')

with open(join(dirname, 'chatid.txt'), 'r+') as f:
    chatid=f.read()
    if chatid.strip()=='':
        click.secho('введите /start в боте',  fg='white', bg='green')
        bot.infinity_polling()
    else:
        conf.chat_id = int(chatid)
        main()

