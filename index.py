# coding: UTF-8
import requests
import datetime
import csv
import time
import re
from bs4 import BeautifulSoup

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2022, 7, 1)

target_date = start_date

# 注釈情報から余計な情報を消す
def clear_tag(array):
    for element in array:
        del element['class']
        del element['data-audio']
        del element['href']
        del element['data-type']

# ファイルオープン
with open("output.csv", "w") as csvptr:

    writer = csv.writer(csvptr, lineterminator='\n')

    while target_date <= end_date:

        # アクセスするURL
        url_prefix = "https://xxx.com/xxx/yyy?ymd="
        url = url_prefix + target_date.strftime("%Y%m%d")

        # html 取得
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        # テキスト取得
        en = soup.find("div", {"id": "english"})
        jp = soup.find("div", {"id": "japanese"})

        if en == None or jp == None:
            target_date = target_date + datetime.timedelta(1)
            print(target_date)
            time.sleep(1.5)
            continue

        # 整形
        en.dl.decompose()
        jp.dl.decompose()
        clear_tag(en.find_all("a"))

        jp_text = ''.join(jp.strings).strip()
        if jp_text == "":
            target_date = target_date + datetime.timedelta(1)
            print(target_date)
            time.sleep(1.5)
            continue

        en_text = ''
        for child in en.contents:
            en_text += str(child)
        en_text = re.sub(r"</?br/?>", "", en_text.strip())

        en_a = en.find_all("a")
        en_text = ''.join(en.strings).strip()
        a_string = ''
        for child in en_a:
            a_string += str(child)
            a_string += "\n"

        writer.writerow([target_date.strftime("%Y-%m-%d"), en_text, jp_text, a_string])

        target_date = target_date + datetime.timedelta(1)
        print(target_date)
        time.sleep(1.5)
