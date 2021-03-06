# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

# coding=gbk
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码, 防止控制台打印乱码
target_year_list = ["2019", "2020"]
target_month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


def get_city_dict(file_path):

    city_dict = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        #        line_list = f.readline()
        for line in file:
            line = line.replace("\r\n", "")
            city_name = (line.split(" ")[0]).strip()
            city_pinyin = ((line.split(" ")[1]).strip()).lower()
            # 赋值到字典中...
            city_dict[city_pinyin] = city_name

    return city_dict


def get_urls(city_pinyin):
    urls = []

    for year in target_year_list:
        for month in target_month_list:
            date = year + month
            urls.append("http://www.tianqihoubao.com/lishi/{}/month/{}.html".format(city_pinyin, date))

    return urls


# url = "http://www.tianqihoubao.com/lishi/beijing/month/201812.html"

file_path = "./city_list.txt"
city_dict = get_city_dict(file_path)


def get_soup(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  # 若请求不成功,抛出HTTPError 异常
        # r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    # except HTTPError:
    #  return "Request Error"
    except Exception as e:
        print(e)
        pass


def saveTocsv(data, city):
    """
    将天气数据保存至csv文件
    """
    fileName = './' + city_dict[city] + '_weather_data.csv'
    result_weather = pd.DataFrame(data, columns=['date', 'tq', 'temp', 'wind'])
    # print(result_weather)
    result_weather.to_csv(fileName, index=False, encoding='gb18030')
    print('Save all weather success!')



def get_data(url):
    print(url)
    try:
        soup = get_soup(url)
        all_weather = soup.find('div', class_="wdetail").find('table').find_all("tr")
        data = list()
        for tr in all_weather[1:]:
            td_li = tr.find_all("td")
            for td in td_li:
                s = td.get_text()
                # print(s.split())
                data.append("".join(s.split()))

        # print(data)
        # print(type(data))
        res = np.array(data).reshape(-1, 4)

        # print(res)
        # print(type(res[0]))
        # print(res[0][1])
        return res

    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':

    for city in city_dict.keys():
        print(city, city_dict[city])
        data_ = list()
        urls = get_urls(city)

        for url in urls:
            try:
                data_.extend(get_data(url))  # 列表合并，将某个城市所有月份的天气信息写到data_
            except Exception as e:
                print(e)
                pass
        saveTocsv(data_, city)  # 保存为csv