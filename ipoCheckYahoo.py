import requests
from bs4 import BeautifulSoup
import re
import datetime

#gmail
from gmail import sendGmail

MAIL_ADR = 'mtake88@gmail.com'
MAIL_PWD = 'jnfzzdwkghwmrgkm'

#-----------------------------
# gmail送信
#-----------------------------
def sendIpoMail(type):
    subject = f'【IPO初値】本日({today})：{len(orderList)}件'
    bodyText = '本日のIPO初値状況\n\n'
    for ll in orderList:
        bodyText += f"■{ll[0]}  初値：{ll[1]}\n"
    sendGmail(MAIL_ADR, MAIL_ADR, MAIL_ADR, MAIL_PWD, subject, bodyText)

def ipoCheckYahoo():

    top_url = "https://info.finance.yahoo.co.jp/ipo/"
    res = requests.get(top_url)
    soup = BeautifulSoup(res.text, "html.parser")
    ipo_infos = soup.find_all('div', class_='ipoBrandBox')
    print(len(ipo_infos))

    for info in ipo_infos:
        order_one = []
        elems = info.select('table > tr:nth-of-type(1) > td.presentation > p > span')
        in_date = datetime.datetime.strptime(elems[0].contents[0], '%Y/%m/%d')
        if today == in_date.date():  # 本日上場のIPO銘柄であるか?
            kobetu_url = info.select_one('table > tr:nth-of-type(1) > td.ttl > h2 > a').get('href')
            kobetu = requests.get(kobetu_url)
            ksoup = BeautifulSoup(kobetu.text, "html.parser")

            print("==============================")
            kmeigara = ksoup.find('h1', class_='stock_name mb-2')
            order_one.append(kmeigara.text)
            print(kmeigara.text)
            kele = ksoup.select(
                "#content_area > div.container-fluid > div > div.col-md-8.col-sm-12.content_main > div:nth-of-type(1) > div:nth-of-type(5) > div.d-flex.flex-md-nowrap.flex-wrap > div:nth-of-type(2) > table > tr:nth-of-type(5) > td")
            kprice = kele[0].contents[0]
            order_one.append(kprice)
            print(kprice)
            orderList.append(order_one)

    # print(orderList)

if __name__ == "__main__":
    orderList = []  # 注文内容をメールで送信

    dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
    today = dt.date()

    ipoCheckYahoo()
    sendIpoMail(0)

    print("complete")

