import requests
from bs4 import BeautifulSoup
import re
import datetime

#gmail
from gmail import sendGmail

MAIL_ADR = 'mtake88@gmail.com'
MAIL_PWD = 'jnfzzdwkghwmrgkm'

errNumber = 0

#-----------------------------
# gmail送信
#-----------------------------
def sendIpoMail(type):
    global errNumber

    if errNumber == 0:
        subject = f'【IPO初値】本日({today})：{len(orderList)}件'
        bodyText = '本日のIPO初値状況\n\n'
        for ll in orderList:
            if str(ll[4])=="*":
                bodyText += f"■[{ll[1]}] {ll[0]}  初値：{ll[3]}\n"
            else:
                bodyText += f"■[{ll[1]}] {ll[0]}  初値：{ll[3]} ({ll[4]:+})\n"

    elif errNumber == -1:
        subject = f'【IPO初値】データの読み込みに失敗した可能性があります。'
        bodyText = 'データ参照元のページ構成が更新された可能性があります。\n\nソースコードを確認してください。\n'

    sendGmail(MAIL_ADR, MAIL_ADR, MAIL_ADR, MAIL_PWD, subject, bodyText)

def ipoCheckYahoo():
    global errNumber

    top_url = "https://www.traders.co.jp/ipo/"
    res = requests.get(top_url)
    soup = BeautifulSoup(res.text, "html.parser")
    ipo_infos = soup.select('#content_area > div.container-fluid > div > div.col-md-8.col-sm-12.content_main > div:nth-child(1) > div:nth-child(5) > div.scrollable.mb-1 > table > tbody > tr')
#    ipo_infos = soup.find_all('th', class_='text-nowrap')
    print(len(ipo_infos))

    if len(ipo_infos) == 0:
        ipo_infos = soup.select('#content_area > div.container-fluid > div > div.col-md-8.col-sm-12.content_main > div:nth-child(1) > div:nth-child(6) > div.scrollable.mb-1 > table > tbody > tr')
        if len(ipo_infos) == 0:
            errNumber = -1

    for info in ipo_infos:
        order_one = []
        jojobi = info.contents[1].contents[0].strip()
        if '/' in jojobi:   #'mm/dd'であるか？
            #if '04/14' == jojobi:  # 本日上場のIPO銘柄であるか?
            if today.strftime("%m/%d") == jojobi:  # 本日上場のIPO銘柄であるか?
                print(today)
                kobetu_url = info.find('a').get('href')
                kobetu_url = "https://www.traders.co.jp" + kobetu_url
                print(kobetu_url)
                kobetu = requests.get(kobetu_url)
                ksoup = BeautifulSoup(kobetu.text, "html.parser")
                kmeigara = ksoup.find('h1', class_='stock_name mb-2')
                print(kmeigara.text)
                order_one.append(kmeigara.text)

                #soup.selectでは、"> tbody" を消して設定する。
                kele = ksoup.select('#content_area > div.container-fluid > div > div.col-md-8.col-sm-12.content_main > div:nth-child(1) > div:nth-child(3) > table > tbody > tr:nth-child(2) > td:nth-child(1)')
                kcode = kele[0].contents[0]
                order_one.append(kcode)
                print(kcode)

                kele = ksoup.select('#content_area > div.container-fluid > div > div.col-md-8.col-sm-12.content_main > div:nth-child(1) > div:nth-child(4) > div.d-flex.flex-md-nowrap.flex-wrap > div:nth-child(2) > table > tr:nth-child(4) > td')
                kkokai = kele[0].contents[0].replace("円","")
                kkokai = kkokai.replace(",","")
                order_one.append(kkokai)
                print(kkokai)

                kele = ksoup.select('#content_area > div.container-fluid > div > div.col-md-8.col-sm-12.content_main > div:nth-child(1) > div:nth-child(4) > div.d-flex.flex-md-nowrap.flex-wrap > div:nth-child(2) > table > tr:nth-child(6) > td')
                kprice = kele[0].contents[0]
                order_one.append(kprice)
                print(kprice)

                if str(kprice).isdigit():
                    kupdw = int(kprice) - int(kkokai)
                else:
                    kupdw = "*"
                order_one.append(kupdw)
                print(kupdw)

                orderList.append(order_one)

if __name__ == "__main__":
    orderList = []  # 注文内容をメールで送信

    dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
    today = dt.date()

    ipoCheckYahoo()
    sendIpoMail(0)

    print("complete")

