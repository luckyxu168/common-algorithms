# 网址为：https://www.xiurenji.cc/
from bs4 import BeautifulSoup
import requests as r
import os
import re
from random import choice
import shutil
import sys
from time import time

UserAgent = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.111 YaBrowser/21.2.1.107 Yowser/2.5 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"]
headers = {"User-Agent": choice(UserAgent)}

def modify_dictionary_name(s):
    start_index = s.find("[")
    return s[start_index:]

def xiurenji_download_single(url):
    page_source_text = r.get(url=url, headers=headers)
    page_source_text.encoding = 'GB2312'
    page_text = page_source_text.text
    soup = BeautifulSoup(page_text, 'lxml')
    # 获取总页数
    pagenumber_moban = r'>\d\d</a>'
    pattern = re.compile(pagenumber_moban)
    match = re.findall(pattern, str(soup))
    page_list = []
    if match:
        for i in match:
            page_list.append(i[1:3])
    else:
        pagenumber_moban = r'>\d</a>'
        pattern = re.compile(pagenumber_moban)
        match = re.findall(pattern, str(soup))
        for i in match:
            page_list.append(i[1:2])
    pagenumbers = int(max(page_list))
    print("网页共有{}页".format(pagenumbers))
    # 下载第一页的图片
    l = soup.find_all('img', onload='size(this)')
    image_url_list = []
    image_url_base = 'https://www.xiurenji.cc'
    kwd = os.getcwd()
    s_d = l[0].get("alt")
    s_d = modify_dictionary_name(s_d)
    print("正在下载套图：{}".format(s_d))
    # 创建文件夹
    if not os.path.exists(kwd + '\\' + s_d):
        os.mkdir(kwd + '\\' + s_d)
    else:
        shutil.rmtree(kwd + '\\' + s_d)
        os.mkdir(kwd + '\\' + s_d)
    picture_numbers = 0
    if pagenumbers < 34:
        picture_numbers_real = int(s_d[-3:-1])
    else:
        picture_numbers_real = int(s_d[-4:-1])
    print("共有{}张图片".format(picture_numbers_real))
    for i in l:
        image_url = image_url_base + i.get("src")
        image_url_list.append(image_url)
    # 下载第1页里面的图片
    for i in range(len(image_url_list)):
        print("正在下载第{}张图片......".format(i + 1))
        img_data = r.get(url=image_url_list[i], headers=headers).content
        img_path = kwd + '\\' + s_d + '\\' + str(i + 1) + ".jpg"
        with open(img_path, 'wb') as fp:
            fp.write(img_data)
        repeat_time = 0
        # 判断此图片是否完整，不是完整的就删除重新下载，如果重新下载的次数超过5次，则退出程序
        while os.path.getsize(img_path) == 315:
            os.remove(img_path)
            img_data = r.get(url=image_url_list[i], headers=headers).content
            img_path = kwd + '\\' + s_d + '\\' + str(i + 1) + ".jpg"
            with open(img_path, 'wb') as fp:
                fp.write(img_data)
            repeat_time += 1
            if repeat_time > 5:
                sys.exit('第{}张图片下载失败，程序退出！'.format(i + 1))
        picture_numbers += 1
        print("第{}张图片下载完成!".format(i + 1))
    # 下载后面网页里面的图片
    for p in range(1, pagenumbers):
        url_later = url[:-5] + "_" + str(p) + ".html"
        page_source_text = r.get(url=url_later, headers=headers)
        page_text = page_source_text.text
        soup = BeautifulSoup(page_text, 'lxml')
        l = soup.find_all('img', onload='size(this)')
        image_url_list = []
        for i in l:
            image_url = image_url_base + i.get("src")
            image_url_list.append(image_url)
        for i in range(len(image_url_list)):
            print("正在下载第{}张图片......".format(picture_numbers + 1))
            img_data = r.get(url=image_url_list[i], headers=headers).content
            img_path = kwd + "\\" + s_d + '\\' + str(picture_numbers + 1) + ".jpg"
            with open(img_path, 'wb') as fp:
                fp.write(img_data)
            repeat_time = 0
            while os.path.getsize(img_path) == 315:
                os.remove(img_path)
                img_data = r.get(url=image_url_list[i], headers=headers).content
                img_path = kwd + '\\' + s_d + '\\' + str(picture_numbers + 1) + ".jpg"
                with open(img_path, 'wb') as fp:
                    fp.write(img_data)
                repeat_time += 1
                if repeat_time > 5:
                    sys.exit('第{}张图片下载失败，程序退出！'.format(picture_numbers + 1))
            print("第{}张图片下载完成!".format(picture_numbers + 1))
            picture_numbers += 1
    # 判断下载图片的数量是否与真实的图片数量一致
    if picture_numbers_real == picture_numbers:
        print("全部{}张图片下载完成!".format(picture_numbers))
        print("套图《{}》下载完成!".format(s_d))
    return picture_numbers


if __name__ == '__main__':
    url_input = input('请输入第一页的网址：')
    start_time = time()
    numbers = xiurenji_download_single(url_input)
    end_time = time()
    run_time = end_time - start_time
    print("用时{}分{}秒，每张图片平均下载时间为{}秒".format(int(run_time / 60), int(run_time % 60), round(run_time / numbers, 2)))
